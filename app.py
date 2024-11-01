from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey
app = Flask(__name__)

app.config['SECRET_KEY'] = 'shhthisismypassword'
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Gets survey from surveys.py
s = satisfaction_survey

'''Displays survey title, instructions and prompts to start the survey'''
@app.route('/')
def start_survey():
    title = s.title
    instructions = s.instructions
    
    return render_template('home.html', title=title, instructions=instructions)

'''Initializes session['responses'] and redirects to begin survey'''
@app.route('/begin-survey', methods=['POST'])
def set_responses():
    session['responses'] = []
    return redirect(f"/questions/{len(session['responses'])}")

'''Displays question according to question_id'''
@app.route('/questions/<int:question_id>')
def question_page(question_id):
    res = session['responses']

        # checks if survey is already completed
    if len(res) == len(s.questions):
        flash('Survey already completed!')

        return render_template('finished.html')
    
        # checks url for correct id
    if question_id == len(res):
        question = s.questions[question_id].question
        choices = s.questions[question_id].choices

        return render_template('questions.html', question=question, question_id=question_id, choices=choices)

    else:
        flash('Trying to access invalid question')

        return redirect(f'/questions/{len(res)}')

'''Appends user answer to responses list, goes to next question if needed or shows finished page.'''
@app.route('/answer', methods=['POST'])
def answer():
    res = session['responses']

    choice = request.form['choice']
    res.append(choice)

    session['responses'] = res

    if len(res) == len(s.questions):
        return render_template('finished.html')

    return redirect(f"/questions/{len(res)}")

