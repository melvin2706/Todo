import sqlite3
from flask import Flask, render_template, redirect, request
from database import get_db_connection

app = Flask(__name__)


# dashbord view function
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# task list view function
@app.route('/tasks')
def AllTasks():
    connect = get_db_connection()
    tasks = connect.execute('select * from task').fetchall()
    connect.close
    task_list = list()
    for task in tasks:
        task_list.append({'id':task['id'], 'name':task['name'], 'description':task['description']})
    return render_template('task/tasks.html', tasks = task_list)

# task detaile view function
@app.route('/task/<int:id>')
def Task(id):
    connect = get_db_connection()
    task = connect.execute('select * from task where id = ?',(str(id))).fetchone()
    connect.close()
    task_detail = {'id':task['id'], 'name':task['name'], 'description':task['description']}
    return render_template('task/taskDetaile.html', task=task_detail)

# add task view function
@app.route('/addTask', methods=['POST','GET'])
def addTask():
    if request.method == 'POST':
        t_name = request.form['name']
        t_description = request.form['description']
        connect = get_db_connection()
        connect.execute("insert into task (name,description) values(?,?)", (t_name, t_description))
        connect.commit()
        connect.close()
        return redirect('/tasks')
    return render_template('task/addTask.html')

@app.route('/delete_redirect/<int:id>')
def delete_redirection(id):
    connect = get_db_connection()
    task = connect.execute('select * from task where id = ?',(str(id))).fetchone()
    connect.close()
    task_detail = {'id':task['id'], 'name':task['name'], 'description':task['description']}
    return render_template('task/deleteTask.html', task=task_detail)
    

# delete view function
@app.route('/deleteTask/<int:id>')
def deleteTask(id):
    connect = get_db_connection()
    connect.execute('delete from task where id= ?', (str(id)))
    connect.commit()
    connect.close()
    return redirect('/tasks')

#update task view function
@app.route('/updateTask/<int:id>', methods=['POST', 'GET'])
def updateTask(id):
    connect = get_db_connection()
    task = connect.execute('select * from task where id = ?',(str(id))).fetchone()
    connect.close()
    task_detail = {'id':task['id'], 'name':task['name'], 'description':task['description']}
    if request.method =='POST':
        u_name = request.form['name']
        u_description = request.form['description']
        connect = get_db_connection()
        connect.execute('update task set name=?, description=? where id =?',(u_name, u_description,str(id)))
        connect.commit()
        connect.close()
        return redirect('/task/'+str(id))
    return render_template('task/updateTask.html', task = task_detail)

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