from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class_course = db.Table('class_course',
                        db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
                        db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
                        )


class Class_entity(db.Model):
    # one class multi courses
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    courses = db.relationship('Course', secondary=class_course, backref=db.backref('classes'))


class Semaster(db.Model):
    # one semaster multi courses
    __tablename__ = 'semasters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    courses = db.relationship('Course', backref='semaster', lazy=True)


class Course(db.Model):
    # one course one time_serial,one semaster,multi classes
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    teacher = db.Column(db.String(12), nullable=False)
    students_num = db.Column(db.Integer, nullable=False)
    # time_serial_id = db.Column(db.Integer, nullable=False)
    # time_serial = db.relationship('Time_serial', backref=db.backref('course', uselist=False), lazy=True)
    time_serial = db.relationship('Time_serial', backref='course', uselist=False, lazy=True)
    semaster_id = db.Column(db.Integer, db.ForeignKey('semasters.id'))
    # class_entity_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    # class_entity = db.relationship('Class_entity', backref=db.backref('courses'), lazy=True)


class Time_serial(db.Model):
    # one time_serial one course
    __tablename__ = 'time_serials'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    start_week = db.Column(db.Integer, nullable=False)
    end_week = db.Column(db.Integer, nullable=False)
    start_class = db.Column(db.Integer, nullable=False)
    end_class = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
