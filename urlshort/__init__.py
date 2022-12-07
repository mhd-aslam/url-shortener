from flask import Flask

def create_app(test_config=None):

	app = Flask(__name__)
	app.secret_key = '8h2tf629h20242gv2h2u2u'

	from . import urlshort
	app.register_blueprint(urlshort.bp)

	return app