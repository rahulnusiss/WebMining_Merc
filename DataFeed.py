# class for feeding data into dynamo
import boto3
import json
from boto3 import resource
from botocore.exceptions import ClientError


class Injection:
    # index: 0 = id, 1 = details, 2 = price, 3 = images
    data = []
    # dynamodb_resource = ''
    # table = ''
    REGION = "ap-southeast-1"
    TABLE_NAME = "cars"

    # name represents id 'primary key'
    def __init__(self, name, image):
        self.data = [name, '', '', image]
        # init dynamo
        self.dynamodb_resource = resource('dynamodb', region_name=self.REGION)
        self.table = self.dynamodb_resource.Table(self.TABLE_NAME)
        # Remove space from id
        self.nameID = self.data[0].replace(' ', '_')

    def __init__(self, name, details, price):
        self.data = [name, details, price, '']
        # init dynamo
        self.dynamodb_resource = resource('dynamodb', region_name=self.REGION)
        self.table = self.dynamodb_resource.Table(self.TABLE_NAME)
        # Remove space from id
        self.nameID = self.data[0].replace(' ', '_')

    def displayData(self):
        print(self.data)

    def prepareJson(self):
        merc_jsondata = {}
        for elem in self.data[1]:
            key = elem[0].replace(':', '')
            merc_jsondata[key] = elem[1]
        merc_json_data = json.dumps(merc_jsondata)
        # print (merc_json_data)
        return merc_json_data

    def injectData(self):
        details_data = self.prepareJson();
        # print (self.data[0])
        # print (details_data)
        # print (self.data[2])

        self.table.put_item(
            Item={
                'id': self.nameID,
                'details': details_data,
                "price": self.data[2]
            }
        )

    def injectImages(self):
        self.table.put_item(
            Item={
                'id': self.nameID,
                'images': self.data[3]
            }
        )

    def deleteItem(self):
        # Remove space from id
        nameID = self.data[0].replace(' ', '_')
        try:
            response = self.table.delete_item(
                Key={
                    'id': self.nameID
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("DeleteItem succeeded:")
            print(json.dumps(response, indent=4))