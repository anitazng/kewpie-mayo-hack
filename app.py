from flask import Flask, redirect, render_template, request
from main import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/create-schedule", methods=["POST", "GET"])
def create_schedule():
    main()
    return redirect("https://calendar.google.com/calendar/u/0/r/day")

if __name__ == '__main__': 
    app.run(debug=True)