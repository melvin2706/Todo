from flask import Flask, render_template, redirect

app = Flask(__name__)

tasks = [
        {'id':1, 'name':'task', 'description':'description'},
        {'id':2, 'name':'task', 'description':'description'},
        {'id':3, 'name':'task', 'description':'description'}
    ]

# dashbord view function
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# task list view function
@app.route('/tasks')
def AllTasks():
    return render_template('task/tasks.html', tasks = tasks)

# task detaile view function
@app.route('/task/<int:id>')
def Task(id):
    for iterable in tasks:
        if iterable['id'] == id:
            task = iterable
    return render_template('task/taskDetaile.html', task=task)

# add task view function
@app.route('/addTask')
def addTask():
    return render_template('task/addTask.html')

# delete view function
@app.route('/deleteTask/<int:id>')
def deleteTask(id):
    for iterable in tasks:
        if iterable['id'] == id:
            task = iterable
    return render_template('task/deleteTask.html', task=task)

#update task view function
@app.route('/updateTask/<int:id>')
def updateTask(id):
    for iterable in tasks:
        if iterable['id'] == id:
            task = iterable
    return render_template('task/updateTask.html', task = task)

# index view function which is our login view function
@app.route('/')
@app.route('/login')
def index():
    return render_template('authen/login.html')

# SignUp view function 
@app.route('/signup')
def registration():
    return render_template('authen/signUp.html')

# logout view function
@app.route('/logout')
def logout():
    return redirect('/login')

@app.route('/profile')
def UserProfile():
    return render_template('user/profile.html')

#error view function
@app.route('/error')
def error():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)