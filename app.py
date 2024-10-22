from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'shhthisismypassword'
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Stores users responses
responses = []

    # Gets survey from surveys.py
s = satisfaction_survey

'''Displays survey title, instructions and prompts to start the survey'''
@app.route('/')
def start_survey():
    title = s.title
    instructions = s.instructions
    
    return render_template('home.html', title=title, instructions=instructions)

'''Displays question according to question_id'''
@app.route('/questions/<int:question_id>')
def question_page(question_id):
        # checks url for correct id
    if question_id == len(responses):
        question = s.questions[question_id].question
        choices = s.questions[question_id].choices

        return render_template('questions.html', question=question, question_id=question_id, choices=choices)
    else:
        flash('Trying to access invalid question')

        return redirect(f'/questions/{len(responses)}')

@app.route('/answer', methods=['POST'])
def answer():
    choice = request.form['choice']
    responses.append(choice)

    if len(responses) == len(s.questions):
        return render_template('finished.html')

    return redirect(f'/questions/{len(responses)}')



