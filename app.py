'''This is a flask app micro service for the dev ops culture and practice course'''
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap

APP = Flask(__name__)

Bootstrap(APP)

@APP.route('/')
@APP.route('/<username>')
def home_page(username='World!'):
    '''A function that renders a web page.  If you user the /<username>
    endpoint the web page will include that word'''
    return render_template('home.html', username=username)


@APP.route('/api/hello/')
@APP.route('/api/hello/<username>')
def api(username='World!'):
    '''A function that returns some json.  The default is a dictionary containing
    Hello: World!.  If the /api/hello/<username> endpoint is hit then you get a more
    interesting response.'''
    return jsonify({'Hello': username})

@APP.route('/api/version/')
def version():
    '''This function returns a dictionary containing only
       the key version with a value set to the application
       version number which is read from a file called VERSION.txt

       The VERSION.txt file is read and the variable version is
       extracted by taking the first line ([0]) and then removing
       any whitespace (like \n from it) with strip().  It's not
       converted to an integer because sometimes versions have letters,
       or dots in them.

       :rtype: A Json object containing version: number'''

    with open("VERSION.txt", "r") as myfile:
        version_number = myfile.readlines()[0].strip()

    return jsonify({'version': version_number})
    