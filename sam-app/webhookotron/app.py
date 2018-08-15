import boto3
import json
import uuid

# Create an S3 client
s3 = boto3.client('s3')

def flattenEvent(item):
    str = ''
    try:
        str = json.dumps(item['msys']['message_event'])
    except:
        pass
    str += "\n"
    return str

def lambda_handler(event, context):
    """Sample pure Lambda function

    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API
        context LambdaContext -- Lambda Context runtime methods and attributes

    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """

    #print(json.dumps(event))

    # Only accept JSON. If the client doesn't specify a Content-Type,
    # assume it's JSON.
    ct = 'application/json'
    try:
        ct = event['headers']['Content-Type']
    except:
        pass
    if ct != 'application/json':
        return {
            "statusCode": 200,
            "body": "Unsupported content type " + event.headers['Content-Type']
        }

    # Make sure we have a unique batch ID
    batch_id = ''
    try:
        batch_id = event['headers']['X-MessageSystems-Batch-ID']
    except:
        pass
    if batch_id == '':
        batch_id = uuid.uuid4()

    # XXX: deduplication of batch IDs. Should we base prefix off timestamp
    # of first event?

    # XXX: base filename off batch ID in input data
    filename = str(batch_id) + '.json'

    # XXX: get this from env var
    bucket_name = 'webhookotron-data'

    # Convert the input JSON as follows:
    #
    # 1) If it's an array, convert it into a multi-line string,
    #    with one JSON object per line.
    #
    # 2) For each object in the array / single object,
    #    flatten the data from msys.message_event.* into *,
    #    to make querying in AWS Athena easier.
    #
    # XXX: Support other webhook event types from
    # https://developers.sparkpost.com/api/webhooks/
    #
    obj = json.loads(event['body'])
    output = ''
    if isinstance(obj, dict):
        output += flattenEvent(obj)
    if isinstance(obj, list):
        for item in obj:
            output += flattenEvent(item)

    s3.put_object(Bucket=bucket_name, Key=filename, ContentType="application/json", Body=output)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "batch_id": str(batch_id),
            "bucket": bucket_name,
            "filename": filename
        })
    }
