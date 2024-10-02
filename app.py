from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = '#10773290705'  # Set a secret key for sessions

#task deponds on three priority
tasks = [
    {"title": "fullstack", "description": "Do the work within 1 day", "priority": "high", "due_date": "2024-09-28"},
    {"title": "backend", "description": "Do the work before 5pm", "priority": "medium", "due_date": "2024-09-27"},
    {"title": "frontend", "description": "Do the work before 4pm", "priority": "low", "due_date": "2024-09-26"}
]


db_config = {
    'user': 'root',#username
    'password': '#10773.R',#sql password
    'host': 'localhost',#local host means your laptop
    'database': 'givetask'#name of the database created in myql
}

# the begining page of the website 
@app.route('/')
def login_page():
    return render_template("login.html")

#it 
@app.route('/submit',methods=['POST'])
def login():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
        
    # Store the name in session to display the name dynamically
    if name:
        session['name'] = name  # Use 'name', for use the current user 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "INSERT INTO users(name, email, password) VALUES ( %s, %s,%s)"
    values = (name, email, password)
        
    try:
        cursor.execute(sql,values)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except mysql.connector.Error as err:
        return f"Error: {err}"
    
@app.route('/homepage')
def home():
    username = session.get('name', 'Guest')  # Default to 'Guest' if not logged in
    return render_template("index.html", username=username, tasks=tasks)

@app.route('/filter-tasks', methods=["GET"])
def filter_task():
    priority = request.args.get("priority")
    due_date = request.args.get("due_date")
    
    filtered_tasks = tasks
    
    # Filter by priority
    if priority:
        filtered_tasks = [task for task in filtered_tasks if task['priority'] == priority]
    
    # Filter by due date
    if due_date:
        filtered_tasks = [task for task in filtered_tasks if datetime.strptime(task['due_date'], "%Y-%m-%d") == datetime.strptime(due_date, "%Y-%m-%d")]
    
    username = session.get('name', 'Guest')  # Fetch the username from session
    return render_template('index.html', tasks=filtered_tasks, username=username)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login_page'))  # Redirect to the login page



if __name__ == "__main__":
    app.run(debug=True, port=3459)
