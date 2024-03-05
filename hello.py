from flask import Flask, render_template,flash
from models.my_form import MyForm
import secrets

secret_key = secrets.token_hex(16)


# create flask instance

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# create a route decorator

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<username>')
def user(username):
    return  render_template("user.html",name=username)


# invalide url
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"),500

@app.route('/name',methods=['GET','POST'])
def name():
        name=None
        form=MyForm()
        if form.validate_on_submit():
            name=form.name.data
            flash('Your name is '+ name)
            form.name.data=''
        return render_template('name.html',form=form,name=name)



