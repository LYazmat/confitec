from boto3 import resource, client
from boto3.dynamodb.conditions import Key
import config
import uuid

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME

client = client(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME
)

resource = resource(
    'dynamodb',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME
)

def check_table(table_name):
    response = client.list_tables()
    if table_name in response['TableNames']:
        return True
    return False

def create_table_artist(): 
    if not check_table('artists'):
        table = resource.create_table(
            TableName = 'artists',
            KeySchema = [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'transaction',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'transaction',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        table.wait_until_exists()

        return table

ArtistTable = resource.Table('artists')

create_table_artist()


def write_to_artist(id, name, songs):
    response = ArtistTable.put_item(
        Item = {
            'id': id,
            'transaction': str(uuid.uuid4()),
            'name': name
        }
    )
    return response

write_to_artist(45, 'Sia', ['Song 1', 'Song 2', 'Song 3'])
'''
def read_from_artist(id):
    response = ArtistTable.get_item(
        Key = {
            'id': id
        },
        AttributesToGet = [
            'id', 'transaction', 'name'
        ]                      
    )
    return response

read_from_artist(45)

'''
response = ArtistTable.query(KeyConditionExpression=Key('id').eq(45))
result = response
[print(i) for i in result['Items']]