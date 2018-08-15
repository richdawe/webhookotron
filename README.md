# webhookotron

Webhook endpoint for SparkPost events

(This is largely a toy project, for my own learning.)

This is a webhook endpoint for use with SparkPost's Webhooks feature.
Currently it will accept and store message_event objects. A later update
may add support for relay_event and ab_test_event. The event data
is stored for 14 days before being expired.

The webhook endpoint runs in Amazon Web Services (AWS). It uses a Lambda function
which is fronted by API Gateway. It provides a public API,
which can be used as the URL for the Webhooks in the SparkPost UI.
The Lambda function performs some minimal transformations to the event data
from SparkPost, before uploading the data into an S3 storage bucket.

The data can be queried in S3 directly using AWS Athena.
This is a manual process. The user needs to write an SQL query
to find the data that they are interested in.

Note: Sample event JSON blobs were copied from https://developers.sparkpost.com/api/webhooks/

TODO: Architecture diagram

## Setup

    mkdir ~/Envs/webhookotron
    virtualenv ~/Envs/webhookotron
    source ~/Envs/webhookotron/bin/activate
    pip install -r requirements.txt

    pip install awscli
    pip install aws-sam-cli

    cd sam-app
    make deploy

Note: S3 bucket names and so on are all hard-coded at the moment,
so the deployment step will likely fail for you. A later update
should make it so anyone can deploy this code to their own AWS account.

Some SQL files are provided for running in AWS Athena:

1) athena-create-table.sql -- This can be pasted and run in the Athena
   query editor to set up the mappings required by Athena to query
   the webhook data stored in S3. Note that not all the JSON fields
   are mapped yet in Athena. You won't be able to query all
   the webhook data in Athena.

2) athena-drop-table.sql -- Drops the database table. Useful during
   development of the mappings in Athena.

3) athena-query-table.sql -- Example Athena query. Repeated here:

    SELECT * FROM webhookotron_events WHERE msg_from LIKE '%@example.com';

