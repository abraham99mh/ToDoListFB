import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import requests
from flask import Flask, render_template, request, abort, Response, session, redirect, flash, url_for
from time import sleep

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sadgdkhjaslfb32r92bjdsf426543h35bwe'

cred = credentials.Certificate("to-do-list-app-api-firebase-adminsdk-z5hjg-56639c0d28.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection('users')

API_KEY = 'AIzaSyBVZ6E4YqiNqPTUcNRMMjUH8iLcsaov5MM'

global ref_user

def login_firebase(email,password):
	data = {"email":email,"password":password,"returnSecureToken":True}
	response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(API_KEY),data=data)
	if response.status_code == 200:
		dicc = response.json()
		user_id = dicc['localId']
		print(user_id)
		return user_id
	if response.status_code == 400:
		print(response.content)
		return False
	

def get_tasks_user(id):
	user_ref = users_ref.document(id)
	user = user_ref.get()
	if user.exists:
		print(user.to_dict())
		tasks_ref = user_ref.collection('tasks')
	else:
		print("El usuario no existe")
		tasks_ref = False
		
	return tasks_ref


def read_tasks(ref):
	docs = ref.get()
	tasks = []
	for doc in docs:
		task = doc.to_dict()
		task['id'] = doc.id
		tasks.append(task)
	print(tasks)
	return tasks


def read_task(ref, id):
	docs = ref.document(id).get()
	print(docs.to_dict())


def create_task(ref, task):
	new_task = {'name':task,'check':False,'fecha': datetime.datetime.now()}
	ref.document().set(new_task)


def update_task(ref, id):
	tasks_ref = ref.document(id).get()
	check = tasks_ref.to_dict()['check']
	print(check)
	if check:
		res = ref.document(id).update({'check':False})
	else:
		res = ref.document(id).update({'check':True})

def update_task_name(ref, id, name):
	res = ref.document(id).update({'name':name})

def delete_task(ref, id):
	res = ref.document(id).delete()
	print(res)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'user_id' in session:
			return redirect(url_for("home"))
		else:
			return render_template('login.html')
	elif request.method == 'POST':
		global ref_user
		email = request.form['email']
		password = request.form['password']
		print(email)
		print(password)
		try:
			user_id = login_firebase(email,password)
			print(f'User id: {user_id}')
			ref_user = get_tasks_user(user_id)
			if user_id:
				session['user_id'] = user_id
				flash('Inicio de sesión completado', 'success')
				return redirect(url_for("home"))
			else:
				print("Sesión fallida")
				flash("Credenciales inválidas", 'danger')
				return redirect(url_for("login"))
		except:
			print("Sesión fallida")
			flash("Credenciales inválidas", 'danger')
			return redirect(url_for("login"))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if 'user_id' in session:
		session.pop('user_id', None)	
	return redirect(url_for("login"))

@app.route('/', methods=['GET', 'POST'])
def home():
	global ref_user
	if request.method == 'GET':
		if 'user_id' in session:
			try:
				print("TASKS")
				tasks = read_tasks(ref_user)	
			except:
				print("Error")
				return abort(404)
			response = {'tasks':tasks, 'counter':len(tasks)}
			return render_template('index.html', response=response, title="ToDoList")
		else:
			return redirect(url_for("login"))
	elif request.method == 'POST':
		newTask = request.form["Task"]
		print(newTask)
		try:
			create_task(ref_user, newTask)
		except:
			pass
			return Response(status=400)
		return Response(status=200)


@app.route('/delete', methods=['POST'])
def delete():
	id = request.form["id"]
	print("DELETE")
	print(id)
	try:
		delete_task(ref_user,id)
		return Response(status=200)

	except:
		pass
		return Response(status=400)


@app.route('/update-check', methods=['POST'])
def updateCheck():
	id = request.form["id"]
	try:
		resp = update_task(ref_user, id)
		return Response(status=200)
	except:
		pass
		return Response(status=400)


@app.route('/update-task-name', methods=['POST'])
def updateName():
	id = request.form["id"]
	name = request.form["nameText"]
	try:
		resp = update_task_name(ref_user, id, name)
		return Response(status=200)
	except:
		pass
		return Response(status=400)


if __name__ == '__main__':
	app.run(debug=True)