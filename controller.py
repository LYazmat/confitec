from boto3 import resource, client
import config
import uuid
import genius
import redisconn

# basically, client instance for check_table
client = client(
    'dynamodb',
    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
    region_name = config.REGION_NAME
)


# Check table in db => True if exists, False otherwise
def check_table(table_name):
    response = client.list_tables()
    if table_name in response['TableNames']:
        return True
    return False


# resource instance from boto3 for other methods/functions
resource = resource(
    'dynamodb',
    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
    region_name = config.REGION_NAME
)

ArtistTable = resource.Table('artists')


# Create table artists, check if it'd been created
def create_table_artists(): 
    if not check_table('artists'):

        table = resource.create_table(
            TableName = 'artists',
            KeySchema = [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Need to wait until table is created
        table.wait_until_exists()

        return {'msg': 'Table created'}

    return {'msg': 'Table already exists'}    


def write_to_artist(artist, cache):

    # Generate a uuid v4
    transaction = str(uuid.uuid4())
    artist['transaction'] = transaction
    ArtistTable.put_item(
        Item = {
            'id': artist['id'],
            'transaction': transaction,
            'name': artist['name']
        }
    )
    if cache:
        # Save Redis
        redisconn.save(artist)


def update_in_artist(artist, cache):
    ArtistTable.update_item(
        Key = {
            'id': artist['id']
        },
        AttributeUpdates={
            'name': {
                'Value'  : artist['name'],
                'Action' : 'PUT'
            }
        }
    )
    if cache:
        # Save Redis
        redisconn.save(artist)
    else:
        # Delete Redis
        redisconn.remove(artist['transaction'])


def read_from_artist(id, cache=True):

    artist = dict()

    # First, check in DynamoDB the ocurrency    
    response = ArtistTable.get_item(
        Key = {
            'id': id
        },
        AttributesToGet = [
            'id', 'transaction', 'name'
        ]                      
    )

    # Check response status code
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if 'Item' in response:
            transaction = response['Item']['transaction']
            if cache:
                # Search on Redis
                artist = redisconn.read(transaction)
                if not artist:
                    # Not found in Redis -> search in genius
                    artist = genius.get_top_songs_by_artist(id)
                    artist['transaction'] = transaction
                    update_in_artist(artist, cache)
                else:
                    artist['from_cache'] = True
            else:
                # Search on genius, update dynamo[and delete redis]
                artist = genius.get_top_songs_by_artist(id)
                artist['transaction'] = transaction
                update_in_artist(artist, cache)
        else:
            artist = genius.get_top_songs_by_artist(id)
            if artist['id']:
                write_to_artist(artist, cache)
            else:
                artist = {'msg': 'Artist not found'}
    else:
        return {
            'status': response['ResponseMetadata']['HTTPStatusCode'],
            'msg': 'Something wrong happened',
            'response': response
        }        
            
    return artist