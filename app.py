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


@app.route("/admin_user")
@login_required
def admin_user():
	data = fetch_all(mysql, "admin_user")
	return render_template('admin_user.html', data=data, table_count=len(data))


@app.route('/edit_admin_user/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_admin_user(modifier_id, act):
	if act == "add":
		return render_template('edit_admin_user.html', data="", act="add")
	else:
		data = fetch_one(mysql, "admin_user", "user_id", modifier_id)
	
		if data:
			return render_template('edit_admin_user.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/comments")
@login_required
def comments():
	data = fetch_all(mysql, "comments")
	return render_template('comments.html', data=data, table_count=len(data))


@app.route('/edit_comments/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_comments(modifier_id, act):
	if act == "add":
		return render_template('edit_comments.html', data="", act="add")
	else:
		data = fetch_one(mysql, "comments", "user_id", modifier_id)
	
		if data:
			return render_template('edit_comments.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/dm")
@login_required
def dm():
	data = fetch_all(mysql, "dm")
	return render_template('dm.html', data=data, table_count=len(data))


@app.route('/edit_dm/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_dm(modifier_id, act):
	if act == "add":
		return render_template('edit_dm.html', data="", act="add")
	else:
		data = fetch_one(mysql, "dm", "follower_id", modifier_id)
	
		if data:
			return render_template('edit_dm.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/follows")
@login_required
def follows():
	data = fetch_all(mysql, "follows")
	return render_template('follows.html', data=data, table_count=len(data))


@app.route('/edit_follows/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_follows(modifier_id, act):
	if act == "add":
		return render_template('edit_follows.html', data="", act="add")
	else:
		data = fetch_one(mysql, "follows", "follower_id", modifier_id)
	
		if data:
			return render_template('edit_follows.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


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
		data = fetch_one(mysql, "ingredients", "ing_id", modifier_id)
	
		if data:
			return render_template('edit_ingredients.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/misuse")
@login_required
def misuse():
	data = fetch_all(mysql, "misuse")
	return render_template('misuse.html', data=data, table_count=len(data))


@app.route('/edit_misuse/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_misuse(modifier_id, act):
	if act == "add":
		return render_template('edit_misuse.html', data="", act="add")
	else:
		data = fetch_one(mysql, "misuse", "reporter_id", modifier_id)
	
		if data:
			return render_template('edit_misuse.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/rates")
@login_required
def rates():
	data = fetch_all(mysql, "rates")
	return render_template('rates.html', data=data, table_count=len(data))


@app.route('/edit_rates/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_rates(modifier_id, act):
	if act == "add":
		return render_template('edit_rates.html', data="", act="add")
	else:
		data = fetch_one(mysql, "rates", "user_id", modifier_id)
	
		if data:
			return render_template('edit_rates.html', data=data, act=act)
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
		data = fetch_one(mysql, "recipes", "rec_id", modifier_id)
	
		if data:
			return render_template('edit_recipes.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/recipes_ingredient")
@login_required
def recipes_ingredient():
	data = fetch_all(mysql, "recipes_ingredient")
	return render_template('recipes_ingredient.html', data=data, table_count=len(data))


@app.route('/edit_recipes_ingredient/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_recipes_ingredient(modifier_id, act):
	if act == "add":
		return render_template('edit_recipes_ingredient.html', data="", act="add")
	else:
		data = fetch_one(mysql, "recipes_ingredient", "rec_id", modifier_id)
	
		if data:
			return render_template('edit_recipes_ingredient.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/reg_user")
@login_required
def reg_user():
	data = fetch_all(mysql, "reg_user")
	return render_template('reg_user.html', data=data, table_count=len(data))


@app.route('/edit_reg_user/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_reg_user(modifier_id, act):
	if act == "add":
		return render_template('edit_reg_user.html', data="", act="add")
	else:
		data = fetch_one(mysql, "reg_user", "user_id", modifier_id)
	
		if data:
			return render_template('edit_reg_user.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/reply_bt")
@login_required
def reply_bt():
	data = fetch_all(mysql, "reply_bt")
	return render_template('reply_bt.html', data=data, table_count=len(data))


@app.route('/edit_reply_bt/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_reply_bt(modifier_id, act):
	if act == "add":
		return render_template('edit_reply_bt.html', data="", act="add")
	else:
		data = fetch_one(mysql, "reply_bt", "requester_id", modifier_id)
	
		if data:
			return render_template('edit_reply_bt.html', data=data, act=act)
		else:
			return 'Error loading #%s' % modifier_id


@app.route("/request_bt")
@login_required
def request_bt():
	data = fetch_all(mysql, "request_bt")
	return render_template('request_bt.html', data=data, table_count=len(data))


@app.route('/edit_request_bt/<string:act>/<int:modifier_id>', methods=['GET', 'POST'])
@login_required
def edit_request_bt(modifier_id, act):
	if act == "add":
		return render_template('edit_request_bt.html', data="", act="add")
	else:
		data = fetch_one(mysql, "request_bt", "requester_id", modifier_id)
	
		if data:
			return render_template('edit_request_bt.html', data=data, act=act)
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
		username = request.form['username']
		password = request.form['password']
		data = fetch_one(mysql, "admin_user", "username", username)
		
		if data and len(data) > 0:
			session['authorised'] = 'authorised',
			session['id'] = data[0]
			session['name'] = data[3]
			session['username'] = data[1]
			session['role'] = 1
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login', error='Wrong Email address or Password.'))
	
	except Exception as e:
		return render_template('login.html', error=str(e))


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)
