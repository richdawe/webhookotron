STACK = webhookotron-app
S3_CODE = webhookotron-code
S3_DATA = webhookotron-data

default:	bucket-stamp build-stamp

# XXX: switch back to build under webhookotron/
build-stamp:	requirements.txt webhookotron/app.py webhookotron/__init__.py
	mkdir -p build
	pip install -U -r requirements.txt -t build
	cp -a  webhookotron/*.py build
	touch $@

bucket-stamp:
	aws s3api list-buckets | grep -q $(S3_CODE) || aws s3 mb s3://$(S3_CODE)
	aws s3api list-buckets | grep -q $(S3_DATA) || aws s3 mb s3://$(S3_DATA)
	aws s3api put-bucket-lifecycle-configuration --bucket $(S3_DATA) --lifecycle-configuration file://s3-data-rules.json
	touch $@

packaged.yaml:	template.yaml
	sam package \
    	--template-file template.yaml \
    	--output-template-file packaged.yaml \
    	--s3-bucket $(S3_CODE)

.PHONY:	deploy
deploy:	packaged.yaml
	sam deploy \
    	--template-file packaged.yaml \
    	--stack-name $(STACK) \
    	--capabilities CAPABILITY_IAM
	aws cloudformation describe-stacks \
    	--stack-name $(STACK) \
    	--query 'Stacks[].Outputs'

clean:
	rm -f bucket-stamp
	rm -rf build
	rm -f build-stamp
