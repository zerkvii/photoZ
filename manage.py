from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/lab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


class Class_entity(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Semaster(db.Model):
    __tablename__ = 'semasters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    teacher = db.Column(db.String(12), nullable=False)
    students_num = db.Column(db.Integer, nullable=False)
    time_serial_id = db.Column(db.Integer, nullable=False)

    class_entity_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    class_entity = db.relationship('Class_entity', backref=db.backref('courses'), lazy=True)


class Time_serial(db.Model):
    __tablename__ = 'time_serials'
    id = db.Column(db.Integer, primary_key=True)
    start_week = db.Column(db.Integer, nullable=False)
    end_week = db.Column(db.Integer, nullable=False)
    start_class = db.Column(db.Integer, nullable=False)
    end_class = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    manager.run()
