from flask import Blueprint, render_template

blueprint = Blueprint('page', __name__)

@blueprint.route('/')
def main_page():
    greet = "Привет Buddy!"
    return render_template('main_page.html', greetings=greet)
