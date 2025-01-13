from flask import Flask, render_template, request

app = Flask(__name__)

progress = {
    "brush_morning": False,
    "shower": False
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global progress
    if request.method == 'POST':
        progress["brush_morning"] = 'brush_morning' in request.form
        progress["shower"] = 'shower' in request.form
    return render_template('profile.html', progress=progress)

if __name__ == '__main__':
    app.run(debug=True)
