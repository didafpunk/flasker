from flask import Flask, render_template, flash,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import secrets
import os
import datetime
from models.my_form import MyForm, UserForm
from werkzeug.security import check_password_hash, generate_password_hash

# csrf gestion clef prive pour les formulaire
secret_key = secrets.token_hex(16)
# create flask instance
app = Flask(__name__)
# secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# Définissez le chemin de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Initialisez SQLAlchemy et Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, created_at={self.created_at})>"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<username>')
def user(username):
    return render_template("user.html", name=username)


# invalide url
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        flash('Your name is ' + name)
        form.name.data = ''
    return render_template('name.html', form=form, name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!')
        else:
            flash('User with this email already exists!')
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.email.data = ''

    users = User.query.all()
    return render_template('add_user.html', form=form, users=users)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        try:
            db.session.commit()
            flash('User edited successfully!')
            return redirect(url_for('add_user',user_id=user.id))
        except:
            flash('Something went wrong')
            return render_template('edit_user.html', form=form, user=user)
    return render_template('edit_user.html', form=form, user=user)



@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('add_user'))  # Redirige vers la page d'ajout d'utilisateur ou une autre page appropriée