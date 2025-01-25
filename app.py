from flask import Flask, render_template, send_from_directory, request
from win11toast import toast
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Progress for checkboxes
progress = {
    "brush_morning": False,
    "shower": False,
    "exercise": False,
    "breakfast": False,
    "wash_hands": False,
    "dinner": False
}

# Dictionary to store scheduled tasks
tasks = {}

# Background thread to monitor tasks
def monitor_tasks():
    while True:
        now = datetime.now().strftime("%H:%M")
        for task, task_time in list(tasks.items()):
            if task_time == now:  # If it's time for the task
                # Use the `toast` function to send a notification
                toast(f"It's time to complete: {task}", "Task Reminder")
                print(f"Notification sent for task: {task}")
                del tasks[task]  # Remove the task after notification (for better organization)
        time.sleep(30)  # Check every 30 seconds

# Start the task monitoring thread
threading.Thread(target=monitor_tasks, daemon=True).start()

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global progress, tasks
    if request.method == 'POST':
        # Save checkbox progress
        for task in progress.keys():
            progress[task] = task in request.form
        
        # Save new tasks
        task_name = request.form.get("task_name")
        task_time = request.form.get("task_time")
        if task_name and task_time:
            tasks[task_name] = task_time

    return render_template('profile.html', progress=progress, tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
