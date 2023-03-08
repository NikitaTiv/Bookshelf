from flask import Blueprint, render_template

blueprint = Blueprint('page', __name__)

@blueprint.route('/')
def main_page():
    return render_template('main_page/main_page.html')
