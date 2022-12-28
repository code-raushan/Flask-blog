import sqlite3

import click
from flask import current_app, g

# g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if 'get_db' is called a second time in the same request.


# current_app is another special object that points to the Flask application handling the request. Since we have used an application factory, there is no application object when writing the rest of our code.

def get_db():
    if 'db' not in g:
        #sqlite3.connect() establishes a db connection.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    #open_resource() opens a file relative to the flaskr package.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# defines a command line command called init-db that calls the init_db() and shows a success message to the user.
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialised the database.')
    
# registering with the application
def init_app(app):
    #app.teardown_appcontext() tells the Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    
    #app.cli.add_command() adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)