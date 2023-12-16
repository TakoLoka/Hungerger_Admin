import hashlib
from flask import Flask, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from handler import *

app = Flask(__name__)
app.secret_key = 'Mage is the best!'

# MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = "takoloka"
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "hungerger"
app.config['MYSQL_DATABASE_HOST'] = "localhost"
mysql.init_app(app)


def login_required(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if 'authorised' not in session:
			return render_template('login.html')
		return f(*args, **kwargs)
	return wrapped


@app.context_processor
def inject_tables_and_counts():
	data = count_all(mysql)
	return dict(tables_and_counts=data)


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')


@app.route("/ingredients")
@login_required
def ingredients():
	data = fetch_all(mysql, "ingredients")
	return render_template('ingredients.html', data=data, table_count=len(data))


@app.route('/edit_ingredients/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_ingredients(modifier_id, act):
	if act == "add":
		return render_template('edit_ingredients.html', data="", act="add")
	else:
		data = fetch_one(mysql, "ingredients", "ingredient_id", modifier_id)
	
		if data:
			return render_template('edit_ingredients.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/recipes")
@login_required
def recipes():
	data = fetch_all(mysql, "recipes")
	return render_template('recipes.html', data=data, table_count=len(data))


@app.route('/edit_recipes/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_recipes(modifier_id, act):
	if act == "add":
		return render_template('edit_recipes.html', data="", act="add")
	else:
		data = fetch_one(mysql, "recipes", "recipe_id", modifier_id)
	
		if data:
			return render_template('edit_recipes.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/recipes_ingredients")
@login_required
def recipes_ingredients():
	data = fetch_all(mysql, "recipes_ingredients")
	return render_template('recipes_ingredients.html', data=data, table_count=len(data))


@app.route('/edit_recipes_ingredients/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_recipes_ingredients(modifier_id, act):
	if act == "add":
		return render_template('edit_recipes_ingredients.html', data="", act="add")
	else:
		data = fetch_one(mysql, "recipes_ingredients", "ri_id", modifier_id)
	
		if data:
			return render_template('edit_recipes_ingredients.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/users")
@login_required
def users():
	data = fetch_all(mysql, "users")
	return render_template('users.html', data=data, table_count=len(data))


@app.route('/edit_users/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_users(modifier_id, act):
	if act == "add":
		return render_template('edit_users.html', data="", act="add")
	else:
		data = fetch_one(mysql, "users", "email", modifier_id)
	
		if data:
			return render_template('edit_users.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route('/save', methods=['GET', 'POST'])
@login_required
def save():
	cat = ''
	if request.method == 'POST':
		post_data = request.form.to_dict()
		if 'password' in post_data:
			post_data['password'] = generate_password_hash(post_data['password']) 
		if post_data['act'] == 'add':
			cat = post_data['cat']
			insert_one(mysql, cat, post_data)
		elif post_data['act'] == 'edit':
			cat = post_data['cat']
			update_one(mysql, cat, post_data, post_data['modifier'], post_data['id'])
	else:
		if request.args['act'] == 'delete':
			cat = request.args['cat']
			delete_one(mysql, cat, request.args['modifier'], request.args['id'])
	return redirect("./" + cat)


@app.route('/login')
def login():
	if 'authorised' in session:
		return redirect(url_for('index'))
	else:
		error = request.args['error'] if 'error' in request.args else ''
		return render_template('login.html', error=error)


@app.route('/login_handler', methods=['POST'])
def login_handler():
	try:
		email = request.form['email']
		password = request.form['password']
		data = fetch_one(mysql, "users", "email", email)
		
		if data and len(data) > 0:
			if check_password_hash(data[3], password) or hashlib.md5(password.encode('utf-8')).hexdigest() == data[3]:
				session['authorised'] = 'authorised',
				session['id'] = data[0]
				session['name'] = data[1]
				session['email'] = data[2]
				session['role'] = data[4]
				return redirect(url_for('index'))
			else:
				return redirect(url_for('login', error='Wrong Email address or Password.'))
		else:
			return redirect(url_for('login', error='No user'))
	
	except Exception as e:
		return render_template('login.html', error=str(e))


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)
