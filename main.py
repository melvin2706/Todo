import sqlite3
from flask import Flask, render_template, redirect, request
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
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

#delete task redirection view function
@app.route('/delete_redirect/<int:id>')
def delete_redirection(id):
    connect = get_db_connection()
    task = connect.execute('select * from task where id = ?',(str(id))).fetchone()
    connect.close()
    task_detail = {'id':task['id'], 'name':task['name'], 'description':task['description']}
    return render_template('task/deleteTask.html', task=task_detail)
    

# delete task view function
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
@app.route('/login', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        connect = get_db_connection()
        user = connect.execute("select * from user where mail = ?;",(mail,)).fetchone()
        connect.close()
        #user_fetched = {'id':user['id'], 'name':user['name'],'mail':user['mail'],'password':user['password']}
        if user:
            if check_password_hash(user['password'],password):
                return redirect('/dashboard')
            else:
                return render_template('authen/login.html', message="Email and password do not match")
            
    return render_template('authen/login.html')

# SignUp view function 
@app.route('/signup', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        password = request.form['password']
        cpassword = request.form['passwordConfirmation']
        if password != cpassword:
            return render_template('authen/signUp.html', message="password and it's confirmation are different")
        else:
            connect = get_db_connection()
            connect.execute("insert into user (name,mail,password) values(?,?,?)", (name, mail,generate_password_hash(password)))
            connect.commit()
            connect.close()
            return redirect('/login')
    return render_template('authen/signUp.html')

# logout view function
@app.route('/logout')
def logout():
    return redirect('/login')

# user profile detail view function
@app.route('/user/<int:id>')
@app.route('/profile/<int:id>')
def UserProfile(id):
    connect = get_db_connection()
    user = connect.execute('select * from user where id = ?',(str(id))).fetchone()
    connect.close()
    user_detail = {'id':user['id'], 'name':user['name'],'mail':user['mail']}
    return render_template('user/profile.html', user=user_detail)

# users list view function
@app.route('/users')
def allUsers():
    connect = get_db_connection()
    users = connect.execute('select * from user').fetchall()
    connect.close
    user_list = list()
    for user in users:
        user_list.append({'id':user['id'], 'name':user['name'],'mail':user['mail']})
    return render_template('user/users.html', users = user_list)


# user update view function
@app.route("/updateInfo/<int:id>", methods=['POST','GET'])
def updateUserInfo(id):
    connect = get_db_connection()
    user = connect.execute('select * from user where id = ?',(str(id))).fetchone()
    connect.close()
    user_detail = {'id':user['id'], 'name':user['name'], 'mail':user['mail']}
    if request.method =='POST':
        u_name = request.form['name']
        u_mail = request.form['mail']
        connect = get_db_connection()
        connect.execute('update user set name=?, mail=? where id =?',(u_name,u_mail,str(id)))
        connect.commit()
        connect.close()
        return redirect('/user/'+str(id))
    return render_template('user/updateUser.html', user = user_detail)


#delete user redirection view function
@app.route('/delete_user_redirect/<int:id>')
def delete_user_redirection(id):
    connect = get_db_connection()
    user = connect.execute('select * from user where id = ?',(str(id))).fetchone()
    connect.close()
    user_detail = {'id':user['id'], 'name':user['name'], 'mail':user['mail']}
    return render_template('user/deleteUser.html', user=user_detail)
    

# delete user view function
@app.route('/deleteUser/<int:id>')
def deleteUser(id):
    connect = get_db_connection()
    connect.execute('delete from user where id= ?', (str(id)))
    connect.commit()
    connect.close()
    return redirect('/users')


#error view function
@app.route('/error')
def error():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)