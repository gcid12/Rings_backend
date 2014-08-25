# Import flask dependencies
from flask import Blueprint, render_template


avispa_web = Blueprint('avispa_web', __name__, url_prefix='/')

# Set the route and accepted methods
@avispa_web.route('/')
@avispa_web.route('/index/', methods=['GET', 'POST'])
def index():

    return render_template("avispa_web/index.html")
