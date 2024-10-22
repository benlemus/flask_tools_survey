from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'shhthisismypassword'
debug = DebugToolbarExtension(app)

# stores users responses
responses = []
s = satisfaction_survey

@app.route('/')
def start_survey():
    title = s.title
    instructions = s.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<int:question>')
def question_page(question):
    question = s.questions[question].question
    return redirect('questions/0')

