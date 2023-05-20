import os

import boto3

def dynamo_table(table_name):
    region = "us-east-1"
    actions_table = boto3.resource(
        "dynamodb", 
        endpoint_url="http://host.docker.internal:4566/",
        region_name=region)
    return actions_table.Table(table_name)