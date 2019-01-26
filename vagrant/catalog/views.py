from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect, flash
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
#may change models import if database name changes

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///itemCatalog.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# TODO: logout page
# TODO: different pages while logged in
# TODO: home buttonns on templates?
# TODO: if <string:cat_name or item_name> results == none : render error template
# TODO: container max-width for templates in place of offset
# TODO: add message flashing
# TODO: add verification that item being created is not currently in the database
# TODO: make pages responsive
# TODO: look into changing title on extended pages

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Catalog App"

@auth.verify_password
def verify_password(username_or_token, password):
	#Try to see if it's a token first
	user_id = User.verify_auth_token(username_or_token)
	if user_id:
		user = session.query(User).filter_by(id = user_id).one()
	else:
		user = session.query(User).filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

# Create anti-forgery state token
@app.route('/login', methods=['GET'])
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
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
		print("Token's client ID does not match app's.")
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								 200)
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

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print("done!")
	return output

	# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session['access_token']
	print('In gdisconnect access token is %s', access_token)
	print('User name is: ')
	print(login_session['username'])
	if access_token is None:
		print('Access Token is None')
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print('result is ')
	print(result)
	if result['status'] == '200':
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/')
@app.route('/catalog')
@app.route('/catalog/')
def viewCategories():
	#this is the main page of the app that displays a list of categories and the latest items added.
	# TODO: One template for username and one without

	categories = session.query(Category).all()
	items = session.query(Item).order_by(desc("id")).limit(10).all()    ## TODO: add modified date/created date?
	return render_template('categories.html', categories=categories, latestItems=items)

@app.route('/catalog/<string:cat_name>')
@app.route('/catalog/<string:cat_name>/items')
def viewIndividual(cat_name):
	#this is the page that will view all items inside a specific category

	categories = session.query(Category).all()
	category = session.query(Category).filter_by(name = cat_name).first()
	items = session.query(Item).filter_by(category_id = category.id).all()

	return render_template('items.html', category = category, items = items, categories = categories)
	# TODO: One template for username and one without

@app.route('/catalog/<string:cat_name>/<string:item_name>')
def viewDescription(cat_name,item_name):
	#this page will be for viewing the description of an items
	# TODO: One template for username and one without

	item = session.query(Item).filter_by(name = item_name).one()

	return render_template('item.html', item = item)

@app.route('/catalog/<string:cat_name>/create', methods=['GET', 'POST'])
# @auth.login_required
def itemCreate(cat_name):
	#this page will be for creating an ITEM
	category = session.query(Category).filter_by(name = cat_name).first()
	if request.method == 'POST':
		if request.form['name'] and request.form['description'] and category.name:
			newItem = Item(name=request.form['name'],
					description=request.form['description'], category=category)
			session.add(newItem)
			session.commit()
			return redirect(url_for('viewIndividual', cat_name = category.name))
		else:

			# TODO: error ridirect to page
			return None
	else:
		return render_template('newItem.html', category= category)

@app.route('/catalog/<string:cat_name>/<string:item_name>/edit', methods=['GET', 'POST'])
# @auth.login_required
def itemEdit(cat_name, item_name):
	#this page will be for editing an ITEM

	editItem = session.query(Item).filter_by(name = item_name).first()
	categories = session.query(Category).all()

	if request.method == 'POST':
		category = session.query(Category).filter_by(name=request.form['category']).first()
		if request.form['name']:
			editItem.name = request.form['name']
		if request.form['description']:
			editItem.description = request.form['description']
		if request.form['category']:
			editItem.category = category
		session.add(editItem)
		session.commit()
		return redirect(url_for('viewIndividual', cat_name = category.name))
	else:
		return render_template('editItem.html', item=editItem, categories=categories)

@app.route('/catalog/<string:cat_name>/<string:item_name>/delete', methods=['GET', 'POST'])
# @auth.login_required
def itemDelete(cat_name, item_name):
	#this page will be for deleting an ITEM

	deleteItem = session.query(Item).filter_by(name = item_name).first()
	category = session.query(Category).filter_by(name=deleteItem.category.name).first()

	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('viewIndividual', cat_name = category.name))
	else:
		return render_template('deleteItem.html', item = deleteItem)

@app.route('/api.json')
def apiAll():
	#returns all items in json format

	categories = session.query(Category).all()
	return jsonify(Category = [c.serialize for c in categories])

@app.route('/api/<string:cat_name>.json')
def apiCategory(cat_name):

	category = session.query(Category).filter_by(name = cat_name).first()
	items = session.query(Item).filter_by(category_id = category.id).all()

	return jsonify(item = [i.serialize for i in items])

@app.route('/api/<string:cat_name>/<string:item_name>.json')
def apiItem(cat_name,item_name):

	category = session.query(Category).filter_by(name = cat_name).first()
	item = session.query(Item).filter_by(category_id = category.id).all()

	return jsonify(item = item.serialize)


if __name__ == '__main__':
	app.debug = True
	app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
	app.run(host='0.0.0.0', port=5000)
