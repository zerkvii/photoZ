from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.security import check_password_hash
from models import *
from flask_login import login_user, logout_user, current_user,login_required

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'easy to guess'
app.debug = True
app.config['FLASK_ENV'] = 'development'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/lab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['FLASK_ENV'] = 'development'
db.init_app(app)
loginManager.init_app(app)
loginManager.login_view = 'login'
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['user']).first() or User.query.filter_by(email=data['user']).first()
        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            info = {
                'type': 'success',
                'information': u'成功登录'
            }
            return jsonify(info), 200
        else:
            info = {
                'type': 'failed',
                'information': u'用户名或密码错误'
            }
            return jsonify(info), 400

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        json_data = request.get_json()
        result = User.insert_user(json_data=json_data)
        if result[0]:
            info = {
                'type': 'success',
                'information': result[1]
            }
            return jsonify(info), 200
            # flash(result[1])
            # print('wqe')
            # return redirect(url_for('login'))
        else:
            info = {
                'type': 'failed',
                'information': result[1]
            }
        return jsonify(info), 400
    return render_template('register.html')


@app.route('/main', methods=['GET'])
@login_required
def main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    manager.run()
