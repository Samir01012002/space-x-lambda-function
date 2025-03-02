import boto3
import requests
import os
from dotenv import load_dotenv
load_dotenv()

DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
SPACEX_API_URL = os.getenv("SPACEX_API")

dynamodb = boto3.resource("dynamodb", aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), region_name=os.getenv("AWS_REGION"))
table = dynamodb.Table(DYNAMODB_TABLE)


def fetch_spacex_launches():
    response = requests.get(SPACEX_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error en la API de SpaceX: {response.status_code}")
        return []

def parse_launch_data(launch):
    return {
        "launch_id": launch.get("id"),
        "order_id": launch.get("id")+"_",
        "mission_name": launch.get("name"),
        "rocket_id": launch.get("rocket"),
        "launch_date": launch.get("date_utc"),
        "status": get_status(launch),
        "launchpad": launch.get("launchpad")
    }

def get_status(launch):
    if(launch.get("upcoming")):
        return "UPCOMING"
    
    if(launch.get("success")):
        return "SUCCESS"
    else:
        return "FAILED"


def save_launch_to_dynamodb(launch_data, table_):
    table_.put_item(Item=launch_data)

def lambda_handler(event, context):
    if "manual" in event and event["manual"]:
        response = table.scan()
        items = response.get("Items", [])
        
        if "count" in event and event["count"]:
            return {"record_count": len(items)}
        return {"records": items}
    
    launches = fetch_spacex_launches()
    for launch in launches:
        parsed_data = parse_launch_data(launch)
        save_launch_to_dynamodb(parsed_data, table)
    
    return {"status": "Data updated successfully", "records_processed": len(launches)}