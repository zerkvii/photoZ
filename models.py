from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager

loginManager = LoginManager()
db = SQLAlchemy()
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

    __table_args__ = (
        db.UniqueConstraint('title', 'teacher', name='unique_course'),
    )

    # class_entity_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    # class_entity = db.relationship('Class_entity', backref=db.backref('courses'), lazy=True)
    #
    @staticmethod
    def add_course(json_data):
        """
        :param json_data:json
        :return:bool,str
        """
        course_title = json_data['title']
        course_teacher = json_data['teacher']
        course_semaster = json_data['semaster']
        course_students_num = json_data['students_num']
        course_classes = json_data['classes']
        course_time_serial = json_data['time_serial']

        semaster = Semaster.query.filter_by(name=course_semaster)

        # time_serial=Time_serial.query.filter_by()
        classes = Class_entity.query.filter(Class_entity.name.in_(course_classes))
        course = Course.query.filter_by(title=course_title).filter_by(teacher=course_teacher).first()
        if not course:
            course = Course(title=course_title, teacher=course_teacher,
                            students_num=course_students_num, semaster=course_semaster,
                            classes=classes, time_serial=course_time_serial)

            course.time_serial = course_time_serial


class Time_serial(db.Model):
    # one time_serial one course
    __tablename__ = 'time_serials'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    start_week = db.Column(db.Integer, nullable=False)
    end_week = db.Column(db.Integer, nullable=False)
    start_class = db.Column(db.Integer, nullable=False)
    end_class = db.Column(db.Integer, nullable=False)

    @staticmethod
    def add_time_serial(json_data):
        """
        :param json_data: json
        :return:bool
        """
        start_week = json_data['start_week']
        end_week = json_data['end_week']
        start_class = json_data['start_class']
        end_class = json_data['end_class']
        if start_week and end_week and start_class and end_class:
            time_serial = Time_serial(start_week=start_week,
                                      end_week=end_week,
                                      start_class=start_class,
                                      end_class=end_class)
            db.session.add(time_serial)
            db.session.commit()
            return True
        else:
            return False


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @staticmethod
    def insert_user(json_data):
        """
        :type json_data: json
        :return:(Bool,str)
        """
        if User.query.filter_by(username=json_data['username']).first() is not None:
            return False, u'用户名已存在'
        elif User.query.filter_by(email=json_data['email']).first() is not None:
            return False, u'邮箱已存在'
        else:
            user = User(username=json_data['username'], email=json_data['email'],
                        password=generate_password_hash(json_data['password']))
            db.session.add(user)
            db.session.commit()
            return True, u'注册用户成功'


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
