from boto3 import resource, client
import config
import uuid
import genius


class ArtistModel:

    def __init__(self):

        self.client = client(
            'dynamodb',
            aws_access_key_id = config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
            region_name = config.REGION_NAME
        )

        self.resource = resource(
            'dynamodb',
            aws_access_key_id = config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
            region_name = config.REGION_NAME
        )

        self.ArtistTable = self.resource.Table('artists')

    def check_table(self, table_name):
        response = self.client.list_tables()
        if table_name in response['TableNames']:
            return True
        return False

    def create_table_artists(self): 
        if not self.check_table('artists'):
            table = self.resource.create_table(
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

            table.wait_until_exists()

            return {'msg': 'Table created'}

        return {'msg': 'Table already exists'}    
    

    def save_in_redis(self, data):
        pass

    def remove_from_redis(self, id):
        pass

    def read_from_redis(self, transaction):
        pass

    def write_to_artist(self, artist):
        transaction = str(uuid.uuid4())
        self.ArtistTable.put_item(
            Item = {
                'id': artist['id'],
                'transaction': transaction,
                'name': artist['name'],
                'cache': artist['cache']
            }
        )
        if artist['cache']:
            # Save Redis set('transaction', json.dumps(artist), ex=7*60*60*24)
            pass

    def update_in_artist(self, artist):
        self.ArtistTable.update_item(
            Key = {
                'id': artist['id']
            },
            AttributeUpdates={
                'name': {
                    'Value'  : artist['name'],
                    'Action' : 'PUT'
                },
                'cache': {
                    'Value'  : artist['cache'],
                    'Action' : 'PUT'
                }
            },
            ReturnValues = "UPDATED_NEW"
        )
        if artist['cache']:
            # Save Redis
            pass
        else:
            # Delete Redis
            pass

    def read_from_artist(self, id, cache=True):

        artist = dict()

        # First, check in DynamoDB the ocurrency    
        response = self.ArtistTable.get_item(
            Key = {
                'id': id
            },
            AttributesToGet = [
                'id', 'transaction', 'name', 'cache'
            ]                      
        )

        # Check response status code
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if 'Item' in response:
                if cache:
                    # Search in Redis
                    # Found -> Return json.loads()
                    # Not Found -> search genius, update dynamo, save redis, return artist
                    pass
                else:
                    # Search genius, update dynamo, delete redis, return artist
                    artist = genius.get_top_songs_by_artist(id)
                    self.update_in_artist(artist)
            else:
                artist = genius.get_top_songs_by_artist(id)
                if artist['id']:
                    artist['cache'] = cache
                    self.write_to_artist(artist)
                else:
                    artist = {'msg': 'Artist not found'}
        else:
            return {
                'status': response['ResponseMetadata']['HTTPStatusCode'],
                'msg': 'Something wrong happened',
                'response': response
            }        
                
        return artist