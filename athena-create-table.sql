CREATE EXTERNAL TABLE webhookotron_events (
	  `type` string,
	  customer_id string,
	  subaccount_id string,
	  transmission_id string,
	  msg_from string,
	  friendly_from string,
	  rcpt_to string,
	  subject string,
	  transactional string,
	  campaign_id string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
LOCATION 's3://webhookotron-data/';
