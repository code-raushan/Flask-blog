import os 
from flask import Flask

def create_app(test_config=None):
    #creating and configuring the app
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_mapping() sets some default configs used by app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        #app.config.from_pyfile() overrides the default configs with values taken from the config.py file in instance folder, if exists.
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        #ensure if app_instance_path exists
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #creating a simple route
    @app.route('/')
    def hello():
        return 'Hello Project'
    
    from . import db
    db.init_app(app)
    return app