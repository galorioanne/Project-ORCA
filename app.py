from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, date, timedelta

app = Flask(__name__)

data_template = {
    "tasks": []}

def due_time_task(datetime):
    now = datetime.now()
    diff = datetime - now

    if diff.total_seconds() < 0:
        return f"Overdue by {-diff.days} days, {-diff.seconds//3600} hours"
    
    if diff.days > 0:
        return f"Due in {diff.days} days"
    
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    return f"Due in {hours}h {minutes}m"


@app.route('/')
def show_tasks():
    try:
        with open('data/data.json', 'r') as file:
            _task = json.load(file)
            task = _task.get("tasks", [])
            for t in task:
                t['datetime'] = datetime.fromisoformat(t['datetime'])
    except FileNotFoundError:
        task = data_template
    return render_template('index.html', data=task, due_time_task=due_time_task)

@app.route('/_addtask', methods=['POST'])
def _addtask():
    return render_template('addtask.html')

@app.route('/addtask_', methods=['GET', 'POST'])
def addtask_():
    try:
        with open('data/data.json', 'r') as file:
            _task = json.load(file)
            task = _task.get("tasks", [])
            for t in task:
                t['datetime'] = datetime.fromisoformat(t['datetime'])
    except FileNotFoundError:
        task = data_template
    
    new_task = {
        "name": request.form['name'],
        "datetime": datetime.fromisoformat(request.form['datetime']),
        "status": False
    }
    task = task + [new_task]
    for t in task:
        t['datetime'] = t['datetime'].isoformat()

    with open('data/data.json', 'w') as file:
        json.dump({"tasks": task}, file, indent=3)

    try:
        with open('data/data.json', 'r') as file:
            _task = json.load(file)
            task = _task.get("tasks", [])
            for t in task:
                t['datetime'] = datetime.fromisoformat(t['datetime'])
    except FileNotFoundError:
        task = data_template

    return render_template('index.html', data=task, due_time_task=due_time_task)

if __name__ == '__main__':
    app.run(debug=True)