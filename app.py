# Web Framework
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flaskwebgui import FlaskUI 

# JSON Handling
import json
from pathlib import Path

# datetime Handling
from datetime import datetime, date, timedelta
import humanize

# System Handling
import sys
import os

DEBUG_MODE = False





app = Flask(__name__)

data_template = { "tasks": [], "schedules": [], "settings": { "theme": "contrast", "date": "%d-%b-%Y", "time": "%I:%M %p", "cardperrow": "5" } }


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Due date and time for TASKS
def due_time_task(due_date):
    now = datetime.now()
    delta = due_date - now

    if delta.total_seconds() < 0:
        return f"Was due {humanize.naturaltime(now - due_date)}"

    if delta < timedelta(days=1):
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        if hours > 0:
            return f"Due in {hours}h and {minutes}m"
        elif minutes > 0:
            return f"Due in {minutes}m"
        else:
            return "Due now"

    else:
        days = delta.days
        if days == 1:
            return "Due in 1 day"
        else:
            return f"Due in {days} days"
    

# Due date and time for SCHEDULES
def due_time_schedule(start_time, end_time):
    now = datetime.now()
    if now < start_time:
        diff = start_time - now
        if diff.days > 0:
            return f"Starts in {diff.days}d" 
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"Starts in {hours}h {minutes}m" 
    elif start_time <= now <= end_time:
        diff = end_time - now
        if diff.days > 0:
            return f"Ends in {diff.days}d" 
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"Ends in {hours}h {minutes}m" 
    else:
        diff = now - end_time
        if diff.days > 0:
            return f"Ended {diff.days}d ago" 
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"Ended {-hours}h {minutes}m ago" 

# Since JSON is ANNOYING and DOESNT SUPPORT DATE TIME OBJECTS,
# IM forced to LEARN THIS so that I CAN USE DATETIME OBJECTS
# WITH JSON BECAUSE OF HOW ANNOYING IT IS.
# SO I HAVE TO CONVERT ISO FORMATS EVERY SINGLE TIME I WANT TO
# ACCESS MY JSON FILE.
def convert_to_iso_format(data):
    for task in data['tasks']:
        if 'datetime' in task and isinstance(task['datetime'], datetime):
            try:
                task['datetime'] = task['datetime'].isoformat()
            except ValueError:
                pass

def parse_iso_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None 

def get_tasks():
    if Path('data/data.json').is_file():
        with open('data/data.json', 'r') as file:
            _task = json.load(file)
            if _task is None:
                _task = {}
            task = _task.get("tasks", [])
            if not task or task == [{}]: # Handle empty list or list with empty dict
                task = []
            else:
                for t in task:
                    t['datetime'] = parse_iso_date(t['datetime'])
    else:
        with open("data/data.json", "w") as file:
            json.dump(data_template, file, indent=3)
            _task = json.load(file)
            task = _task.get("tasks", [])
    return task

def get_schedules():
    if Path('data/data.json').is_file():
        with open('data/data.json', 'r') as file:
            _schedule = json.load(file)
            if _schedule is None:
                _schedule = data_template
                schedule = _schedule.get("schedules", [])
            else:
                schedule = _schedule.get("schedules", [])
            if not schedule or schedule == [{}]: # Handle empty list or list with empty dict
                schedule = []
            else:
                for s in schedule:
                    s['start_time'] = parse_iso_date(s['start_time'])
                    s['end_time'] = parse_iso_date(s['end_time'])
    else:
        with open("data/data.json", "w") as file:
            json.dump(data_template, file, indent=3)
            _schedule = json.load(file)
            schedule = _schedule.get("schedules", [])
    return schedule

def get_settings():
    if Path('data/data.json').is_file():
        with open('data/data.json', 'r') as file:
            _settings = json.load(file)
            if _settings is None:
                _settings = data_template
                settings = _settings.get("settings", {})
            else:
                if "settings" in _settings:
                    settings = _settings.get("settings", [])
                else:
                    with open("data/data.json", "w") as file:
                        json.dump(data_template, file, indent=3)
                    with open('data/data.json', 'r') as file:
                        _settings = json.load(file)
                        if _settings is None:
                            _settings = data_template
                            settings = _settings.get("settings", {})
                        else:
                            settings = _settings.get("settings", [])

    else:
        with open("data/data.json", "w") as file:
            json.dump(data_template, file, indent=3)
        with open('data/data.json', 'r') as file:
            _settings = json.load(file)
            if _settings is None:
                _settings = data_template
                settings = _settings.get("settings", {})
            else:
                settings = _settings.get("settings", [])
    return settings

@app.route('/')
def index():
    print(get_settings())
    return render_template('index.html', tasks=get_tasks(), schedules=get_schedules(), settings=get_settings(), due_time_task=due_time_task, due_time_schedule=due_time_schedule)

@app.route('/viewtasks', methods=['GET'])
def viewtasks():
    return render_template('task.html',tasks=get_tasks(), settings=get_settings(),due_time_task=due_time_task)

@app.route('/viewschedules', methods=['GET'])
def viewschedules():
    return render_template('schedule.html',schedules=get_schedules(), settings=get_settings(),due_time_schedule=due_time_schedule)




# == ADD TASK ==
@app.route('/_addtask', methods=['GET'])
def _addtask():
    return render_template('addtask.html' , message=request.args.get('message', ''), settings=get_settings())

@app.route('/addtask_', methods=['POST'])
def addtask_():
    task = get_tasks()
    
    new_task = { # Creates new task with the name and datetime from the form
        "name": request.form['name'],
        "datetime": datetime.fromisoformat(request.form['datetime']),
        "description": request.form.get('description', ''),
        "status": False
    }

    for t in task:
        if t['name'] == new_task['name']:
            return redirect(url_for('_addtask', message="ERROR: Task with that name already exists."))

    task = task + [new_task]
    for t in task:
        t['datetime'] = t['datetime'].isoformat()
    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["tasks"] = task
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)

    return redirect(url_for("viewtasks")) 



# == REMOVE TASK ==
@app.route('/_removetask', methods=['GET'])
def _removetask():
    return render_template('removetask.html', data=get_tasks(), settings=get_settings())

@app.route('/removetask_', methods=['POST'])
def removetask_():
    task = get_tasks()
    task = [t for t in task if t['name'] != request.form['name']] # Removes the task with the name from the form
    for t in task:
        t['datetime'] = t['datetime'].isoformat()
    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["tasks"] = task
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)
    return redirect(url_for("viewtasks"))




# == EDIT TASK ==
@app.route('/_edittask', methods=['GET'])
def _edittask():
    task_name = request.args.get('task_name')
    task = [t for t in get_tasks() if t['name'] == task_name]
    if task:
        task = task[0]
    return render_template('edittask.html', task=task, settings=get_settings(), message=request.args.get('message', ''))

@app.route('/edittask_', methods=['POST'])
def edittask_():
    task = get_tasks()
    counter = 0
    for t in task:
        if t['name'] == request.form['name']:
            if not t['name'] == request.args.get('task_name'):
                counter += 1
            if counter == 1:
                return redirect(url_for('_edittask', task_name=request.args.get('task_name'), message="ERROR: Task with that name already exists."))

    for t in task:
        if t['name'] == request.args.get('task_name'):
            t['name'] = request.form['name']
            t['datetime'] = datetime.fromisoformat(request.form['datetime'])
            t['description'] = request.form.get('description', '')
            t['status'] = request.form.get('status') == 'on'
        t['datetime'] = t['datetime'].isoformat()

    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["tasks"] = task


    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)
    return redirect(url_for("viewtasks"))



# == ADD SCHEDULE ==
@app.route('/_addschedule', methods=['GET'])
def _addschedule():
    return render_template('addschedule.html', message=request.args.get('message', ''), settings=get_settings())

@app.route('/addschedule_', methods=['POST'])
def addschedule_():
    schedule = get_schedules()
    
    if request.form['end_time'] < request.form['start_time']:
        return redirect(url_for('_addschedule', message="ERROR: End time must be after start time."), settings=get_settings())
    new_schedule = { # Creates new schedule with the name and datetime from the form
        "name": request.form['name'],
        "start_time": datetime.fromisoformat(request.form['start_time']),
        "end_time": datetime.fromisoformat(request.form['end_time']),
        "description": request.form.get('description', '')
    }

    for s in schedule:
        if s['name'] == new_schedule['name']:
            return redirect(url_for('_addschedule', message="ERROR: Schedule with that name already exists.", settings=get_settings()))

    schedule = schedule + [new_schedule]
    for s in schedule:
        s['start_time'] = s['start_time'].isoformat()
        s['end_time'] = s['end_time'].isoformat()
    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["schedules"] = schedule
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)

    return redirect(url_for("viewschedules"))



# == REMOVE SCHEDULE ==
@app.route('/_removeschedule', methods=['GET'])
def _removeschedule():
    return render_template('removeschedule.html', data=get_schedules(), settings=get_settings())

@app.route('/removeschedule_', methods=['POST'])
def removeschedule_():
    schedule = get_schedules()
    schedule = [s for s in schedule if s['name'] != request.form['name']] # Removes the schedule with the name from the form
    for s in schedule:
        s['start_time'] = s['start_time'].isoformat()
        s['end_time'] = s['end_time'].isoformat()
    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["schedules"] = schedule
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)
    return redirect(url_for("viewschedules"))



# == EDIT SCHEDULE ==
@app.route('/_editschedule', methods=['GET'])
def _editschedule():
    schedule_name = request.args.get('schedule_name')
    schedule = [s for s in get_schedules() if s['name'] == schedule_name]
    if schedule:
        schedule = schedule[0]
    return render_template('editschedule.html', schedule=schedule, message=request.args.get('message', ''), settings=get_settings())

@app.route('/editschedule_', methods=['POST'])
def editschedule_():
    schedule = get_schedules()

    counter = 0
    for s in schedule:
        if s['name'] == request.form['name']:
            if not s['name'] == request.args.get('schedule_name'):
                counter += 1
            if counter == 1:
                return redirect(url_for('_editschedule', schedule_name=request.args.get('schedule_name'), message="ERROR: Schedule with that name already exists."), settings=get_settings())
    for s in schedule:
        if s['name'] == request.args.get('schedule_name'):
            if request.form['end_time'] < request.form['start_time']:
                return redirect(url_for('_editschedule', schedule_name=s['name'], message="ERROR: End time must be after start time."), settings=get_settings())
            s['name'] = request.form['name']
            s['start_time'] = datetime.fromisoformat(request.form['start_time'])
            s['end_time'] = datetime.fromisoformat(request.form['end_time'])
            s['description'] = request.form.get('description', '')
        s['start_time'] = s['start_time'].isoformat()
        s['end_time'] = s['end_time'].isoformat()

    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["schedules"] = schedule


    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)
    return redirect(url_for("viewschedules"))


# == SETTINGS ==
@app.route('/_settings', methods=['GET'])
def _settings():
    themes = {}

    theme_folder = Path('themes/')
    for file in theme_folder.iterdir():
        if file.is_file():
            with open(file, 'r') as f:
                f.readline()  # Skip first line
                second_line = f.readline()
                themes[file.stem.replace("theme-", "")] = second_line.strip().replace("/*", "").replace("*/", "")
    print(themes)
    return render_template('settings.html', data=get_schedules(), settings=get_settings(),themes=themes)

@app.route('/settings_', methods=['POST'])
def settings_():
    settings = {
        "theme":request.form["theme"],
        "date":request.form["date"],
        "time":request.form["time"],
        "cardperrow":request.form["cardperrow"]
    }
    with open('data/data.json', 'r') as file:
        data = json.load(file)
        data["settings"] = settings
    with open('data/data.json', 'w') as file:
        json.dump(data, file, indent=3)
    return redirect(url_for("index"))

@app.route('/themes/<path:filename>')
def themes(filename):
    return send_from_directory('themes', filename)










if __name__ == '__main__':
    if DEBUG_MODE == True:
        app.run(debug=True)
    else:
        FlaskUI(app=app, server="flask", fullscreen=True).run()
