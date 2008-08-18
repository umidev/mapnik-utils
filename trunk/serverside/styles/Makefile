all: simplejson cssutils
	#

simplejson:
	curl -sO "http://pypi.python.org/packages/source/s/simplejson/simplejson-1.9.2.tar.gz"
	tar -xzf simplejson-1.9.2.tar.gz
	mv simplejson-1.9.2/simplejson ./
	rm -rf simplejson-1.9.2 simplejson-1.9.2.tar.gz

cssutils:
	curl -sO "http://pypi.python.org/packages/source/c/cssutils/cssutils-0.9.5.1.zip"
	unzip cssutils-0.9.5.1.zip
	mv cssutils-0.9.5.1/src/cssutils ./
	mv cssutils-0.9.5.1/src/encutils ./cssutils/
	rm -rf cssutils-0.9.5.1 cssutils-0.9.5.1.zip

clean:
	rm -rf simplejson
	rm -rf cssutils
