

from flask import Flask
from flask import g

import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(

        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DB_HOST = 'localhost',
        DB_PORT = 6379,
        DB_NO = 0
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import resume
    app.register_blueprint(resume.bp)
    app.add_url_rule('/', endpoint='resume.index')

    return app

# export FLASK_APP=ACMResumeWebsite
# export FLASK_ENV=development
# flask run