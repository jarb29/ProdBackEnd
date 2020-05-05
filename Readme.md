- Markdown Library - https://www.markdownguide.org/basic-syntax/
​
### Step 1: 
    Make a file called Pipfile
​
### Step 2:
Activate virtualenv with pipenv
​
    $ pipenv shell 
​
### Step 3:
With virtualenv activated install the next libraries.
​
    $ pipenv install flask flask-cors flask-migrate flask-sqlalchemy flask-jwt-extended flask-script flask-bcrypt flask-mail
​
The documentation of libraries:
​
- flask - https://palletsprojects.com/p/flask/
- flask-cors - https://flask-cors.corydolphin.com/en/latest/api.html#extension
- flask-script - https://flask-script.readthedocs.io/en/latest/
- flask-migrate - https://flask-migrate.readthedocs.io/en/latest/
- flask-sqlalchemy - https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- flask-jwt-extended - https://flask-jwt-extended.readthedocs.io/en/stable/
- flask-bcrypt - https://flask-bcrypt.readthedocs.io/en/latest/
- flask-mail - https://pythonhosted.org/Flask-Mail/
​
### Step 4:
Make a new file called manage.py as main app.
​
### Step 5:
Write inside the manage.py the next code:
​
    from flask import Flask
​
    app = Flask(__name__)
​
​
    if __name__ == '__main__':
        app.run()
​
### Step 6:
Make a folder called templates
​
    $ mkdir templates
​
Inside of templates make a file called index.html
​
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>API REST FLASK</h1>
    </body>
    </html>
​
### Step 7:
Add the next code into manage.py
    from flask import Flask, render_template
    ...
    @app.route('/')
    def root():
        return render_template('index.html')
    ...
### Step 8:
Make a file called **models.py** with the next code:
​
    from flask_sqlalchemy import SQLAlchemy
​
    db = SQLAlchemy()
​
### Step 9:
Add the next imports into **manage.py**
    ...
    from flask_migrate import Migrate, MigrateCommand
    from flask_script import Manager
    from models import db
    
    ...
    db.init_app(app)
    Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    ...
    
    Before
    @app.route...
​
### Step 10:
Config the flask app with the next options:
​
    app.url_map.strict_slashes = False
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
​
SQLALCHEMY_DATABASE_URI:
- MySQL = mysql://user:password@host:port/dbname
- SQLite = sqlite:///path/to/the/database/file.db
- PostgreSQL = postgresql://user:password@host/database
​
### Step 11:
Config base directory of the app
​
    import os
    ...
​
Make a variable called BASE_DIR with the next code:
​
    from ...
​
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
​
    app ...
​
Change SQLALCHEMY_DATABASE_URI With:
​
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
​
Change app.run() by:
    manager.run()
​
### Step 12:
Generate database, migrations and tables
​
    python app.py db init -- only the first time
    python app.py db migrate -- generate the migrations
    python app.py db upgrade -- update the database
​
​
### Step 13 
Start the server with the next command
​
    $ python manage.py runserver --host=0.0.0.0 --port=9000
Collapse




Message #santiago-part-time-vii


