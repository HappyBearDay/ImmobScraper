from flask import render_template, request, Blueprint
main = Blueprint("main", __name__)


@main.route('/')
@main.route('/home')
def home():
    print("home")
    announces = "hello"
    #return str(announces)
    return render_template("home.html",title="about", announces= announces )