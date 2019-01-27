from flask import Flask, jsonify, request, url_for, abort, g, render_template
from flask import redirect, flash
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
from models import Base, User, Item, Category
import json
import random
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import requests
from flask import make_response
import string

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///itemCatalog.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# TODO: make pages responsive
# TODO: Add in non gmail logins

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Catalog App"


@auth.verify_password
def verify_password(username_or_token, password):
    if 'username' in login_session:
        return True
    return False


# Create anti-forgery state token
@app.route('/login', methods=['GET'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode())
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("""Current user is already
                                            connected."""), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # if username does not exit, add to database
    user = session.query(User).filter_by(username=login_session['username'])\
                  .first()
    if user is None:
        newUser = User(username=login_session['username'])
        session.add(newUser)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("User has been logged out")
        return redirect(url_for('viewCategories'))
    else:
        response = make_response(json.dumps("""Failed to revoke token for given
                                             user.""", 400))
        response.headers['Content-Type'] = 'application/json'
        flash("Error revoking token from the user")
        return redirect(url_for('viewCategories'))


@app.route('/')
@app.route('/catalog')
@app.route('/catalog/')
def viewCategories():
    # this is the main page of the app that displays a list of categories and
    # the latest items added.

    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc("id")).limit(10).all()
    return render_template('categories.html', categories=categories,
                           latestItems=items)


@app.route('/catalog/<string:cat_name>')
def viewIndividual(cat_name):
    # this is the page that will view all items inside a specific category

    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=cat_name).first()
    if category is None:
        return render_template('error.html')
    items = session.query(Item).filter_by(category_id=category.id).all()

    return render_template('items.html', category=category, items=items,
                           categories=categories)


@app.route('/catalog/<string:cat_name>/<string:item_name>')
def viewDescription(cat_name, item_name):
    # this page will be for viewing the description of an items
    category = session.query(Category).filter_by(name=cat_name).first()
    if category is None:
        return render_template('error.html')
    item = session.query(Item).filter_by(name=item_name,
                                         category=category).first()
    if item is None:
        return render_template('error.html')

    return render_template('item.html', item=item)


@app.route('/create/<string:cat_name>', methods=['GET', 'POST'])
@auth.login_required
def itemCreate(cat_name):
    # this page will be for creating an ITEM
    category = session.query(Category).filter_by(name=cat_name).first()
    if category is None:
        return render_template('error.html')
    if request.method == 'POST':
        if (session.query(Item).filter_by(name=request.form['name'],
                                          category=category)
                   .first() is not None):
            flash("Item is already in category, please use edit")
            return redirect(url_for('viewIndividual', cat_name=category.name))
        if (request.form['name'] and request.form['description'] and
           category.name):
            user = session.query(User)\
                          .filter_by(username=login_session['username']).one()
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           category=category, user=user)
            session.add(newItem)
            session.commit()
            return redirect(url_for('viewIndividual', cat_name=category.name))
        else:

            flash("Error creating item, please try again")
            return redirect(url_for('viewCategories'))
    else:
        return render_template('newItem.html', category=category)


@app.route('/catalog/<string:cat_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
@auth.login_required
def itemEdit(cat_name, item_name):
    # this page will be for editing an ITEM
    category = session.query(Category).filter_by(name=cat_name).first()
    if category is None:
        return render_template('error.html')

    editItem = session.query(Item).filter_by(name=item_name,
                                             category=category).first()
    if editItem is None:
        return render_template('error.html')
    categories = session.query(Category).all()

    if request.method == 'POST':
        category = session.query(Category)\
                          .filter_by(name=request.form['category']).first()
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['category']:
            editItem.category = category
        session.add(editItem)
        session.commit()
        return redirect(url_for('viewIndividual', cat_name=category.name))
    else:
        return render_template('editItem.html', item=editItem,
                               categories=categories)


@app.route('/catalog/<string:cat_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
@auth.login_required
def itemDelete(cat_name, item_name):
    # this page will be for deleting an ITEM

    category = session.query(Category).filter_by(name=cat_name).first()
    if category is None:
        return render_template('error.html')

    deleteItem = session.query(Item).filter_by(name=item_name,
                                               category=category).first()
    if deleteItem is None:
        return render_template('error.html')

    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('viewIndividual', cat_name=category.name))
    else:
        return render_template('deleteItem.html', item=deleteItem)


@app.route('/api.json')
def apiAll():
    # returns all items in json format

    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])


@app.route('/api/<string:cat_name>.json')
def apiCategory(cat_name):

    category = session.query(Category).filter_by(name=cat_name).first()
    items = session.query(Item).filter_by(category_id=category.id).all()

    return jsonify(item=[i.serialize for i in items])


@app.route('/api/<string:cat_name>/<string:item_name>.json')
def apiItem(cat_name, item_name):

    category = session.query(Category).filter_by(name=cat_name).first()
    item = session.query(Item).filter_by(category_id=category.id).first()

    return jsonify(item=item.serialize)


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase +
                                       string.digits) for x in range(32))
    app.run(host='0.0.0.0', port=5000)
