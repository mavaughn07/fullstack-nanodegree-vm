from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, g, render_template, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
from models import Base, User, Item, Category
#may change models import if database name changes

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# TODO: Google OAUTH
# TODO: API rate limiting?
# TODO: logout page
# TODO: on items.html Jquery to change item from (1 items) to (1 item)
# TODO: editing items
# TODO: deleting items
# TODO: different pages while logged in
# TODO: home buttonns on templates?
# TODO: if <string:cat_name or item_name> results == none : render error template
# TODO: container max-width for templates in place of offset
# TODO: add message flashing
# TODO: add verification that item being created is not currently in the database



#Fake categories/items
category = {'name' : 'Snowbaoarding', 'id' : '1'}
categories = [{'name' : 'Snowbaoarding', 'id' : '1'},{'name' : 'Soccer', 'id' : '2'},{'name' : 'Baseball', 'id' : '3'}]
item = {'name':'Snowboard','id':'1','description':'goofy style'}
items = [{'name':'Snowboard','id':'1','description':'goofy style'},{'name':'ball','id':'2','description':'jabulani'},{'name':'bat','id':'3','description':'mizuno'}]

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

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.route('/')
@app.route('/catalog')
def viewCategories():
    #this is the main page of the app that displays a list of categories and the latest items added.
    # TODO: One template for username and one without

    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc("id")).limit(10).all()
    return render_template('categories.html', categories=categories, latestItems=items)

@app.route('/catalog/<string:cat_name>')
@app.route('/catalog/<string:cat_name>/items')
def viewIndividual(cat_name):
    #this is the page that will view all items inside a specific category

    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = cat_name).first()
    items = session.query(Item).filter_by(category_id = category.id).all()


    # TODO: check for error in category.id
    return render_template('items.html', category = category, items = items, categories = categories)
    # TODO: One template for username and one without

@app.route('/catalog/<string:cat_name>/<string:item_name>')
def viewDescription(cat_name,item_name):
    #this page will be for viewing the description of an items
    # TODO: One template for username and one without
    # TODO: check relationship between item and category

    category = session.query(Category).filter_by(name=cat_name).first()
    item = session.query(Item).filter_by(name = item_name).one()


    # TODO: check for error in category.id
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
        # TODO: possible error test for category_id change as well


            # TODO: error ridirect to page
            return None
    else:
        # TODO: pass in category names for dropdown box

        print category
        return render_template('newItem.html', category= category)

@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
@auth.login_required
def itemEdit(item_name):
    #this page will be for editing an ITEM


    editItem = session.query(Item).filter_by(name = item_name).first()
    editItem = item


    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['category']:
            editItem.category = request.form['category']
        session.add(editItem)
        session.commit()
        return redirect(url_for('category', cat_name = category))
        # TODO: possible error test for category_id change as well
    else:
        # TODO: pass in category names for dropdown box
        return render_template('editItem.html', item_name = item_name)

@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
@auth.login_required
def itemDelete(item_name):
    #this page will be for deleting an ITEM


    deleteItem = session.query(Item).filter_by(name = item_name).first()
    deleteItem = item

    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('category', cat_name = category))
        # TODO: possible error test for category_id change as well
    else:
        return render_template('deleteItem.html', item_name = item_name)

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

@app.route('/users', methods = ['POST'])
def new_user():
    # TODO: redirect to categories page with message flash
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username = username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200, {'Location': url_for('get_user', id = user.id, _external = True)}

    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}




if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
