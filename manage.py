from flask import Flask, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/lab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # data=request.
        print(request.get_data())
    return render_template('index.html')


if __name__ == '__main__':
    manager.run()
