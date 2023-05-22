import datetime
import uuid
import json
from dynamodb import dynamo_table

def create(event):
    action: dict[str, str] = json.loads(event["body"])
    params = {
        "id": str(uuid.uuid4()),
        "created_dt": str(datetime.datetime.now()),
        "name": action['name'],
        "nickname": action['nickname'],
        "email": action['email']
    }
    db_response = dynamo_table('Actions').put_item(Item=params)
    return {"statusCode": 200, "body": json.dumps(params)}

def list():
    actions_details = dynamo_table('Actions').scan()
    response: dict[str, list | dict] = {"items": actions_details["Items"]}
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(response),
    }

def delete(event):
    action_id: str = event["queryStringParameters"]["id"]
    action_date: str = event["queryStringParameters"]["date"]
    db_response = dynamo_table('Actions').delete_item(
        Key={"id": action_id, "created_dt": action_date},
        ConditionExpression="attribute_exists(id) and attribute_exists(created_dt)",
    )
    return {
        "statusCode": 200,
        "body": "Deleted with success",
    }

def update(event):

    action: dict[str, str] = json.loads(event["body"])
    search_params = {
        "id": str(event["queryStringParameters"]["id"]),
        "created_dt": str(event["queryStringParameters"]["date"]),
    }
    db_response = dynamo_table('Actions').update_item(
        Key=search_params,
        UpdateExpression="set #fn=:n, nickname=:nn, email=:e",
        ExpressionAttributeValues={
            ":n": action["name"],
            ":nn": action["nickname"],
            ":e": action["email"],
        },
        ExpressionAttributeNames={
            "#fn": "name"
        })
    return {
        "statusCode": 200,
        "body": "Update with success",
    }

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return list()
    elif event['httpMethod'] == 'POST':
        return create(event)
    elif event['httpMethod'] == 'DELETE':
        return delete(event)
    elif event['httpMethod'] == 'PUT':
        return update(event)
    else:
        return {"statusCode": 500, "headers": {}, "body": "Internal Server Error"}