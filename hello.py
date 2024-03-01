from flask import Flask, render_template

# create flask instance

app = Flask(__name__)


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