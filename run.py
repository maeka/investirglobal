from app import manager, app
from waitress import serve

if __name__ == '__main__':
	#manager.run()
	serve(app)