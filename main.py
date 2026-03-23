import datetime
import os

from flask import Flask, render_template, redirect, request, make_response, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_restful import reqparse, abort, Api, Resource

from flask_migrate import Migrate

from data import jobs_api
from data.db_init import db
from data.users import User
from data.jobs import Jobs

from forms.loginform import RegisterForm, LoginForm
from forms.jobsform import JobsForm

from data import users_resource

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db')
if not os.path.exists(db_path):
    os.makedirs(db_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, "mars_explorer.db")}?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(jobs_api.blueprint)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/')
def index():
    jobs = db.session.query(Jobs)
    return render_template('index.html', jobs=jobs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registerform.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('registerform.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.about.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('registerform.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('loginform.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('loginform.html', title='Авторизация', form=form)

@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route("/add_job", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        db.session.add(job)
        db.session.commit()
        return redirect("/")
    return render_template('addjobform.html', form=form)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def main():
    app.run(host='0.0.0.0', port=5050, debug=True)


if __name__ == '__main__':
    main()
