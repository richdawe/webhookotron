default:	build-stamp

# XXX: switch back to build under webhookotron/
build-stamp:	requirements.txt webhookotron/app.py webhookotron/__init__.py
	mkdir -p build
	pip install -U -r requirements.txt -t build
	cp -a  webhookotron/*.py build
	touch $@

clean:
	rm -rf build
	rm -f build-stamp
