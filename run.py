from app import manager, app
import os
from waitress import serve


if __name__ == '__main__':
	if 'DYNO' in os.environ:
		serve(app, url_scheme='https')
	else:
		manager.run()


#if 'DYNO' in os.environ:
	#sslify = SSLify(app, permanent=True)  # only trigger SSLify if the app is running on Heroku
	#print(sslify)