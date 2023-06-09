from flask import Flask, request, render_template, flash, session, redirect
#from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

#debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """Show survey title and instructions"""

    return render_template('surveys.html', survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Create answer list and start the survey"""

    session['answers'] = []

    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Show question"""

    answers = session['answers']

    if (answers is None):
        flash("You need to start the survey!")
        return redirect('/')
        
    if (len(answers) == len(satisfaction_survey.questions)):
        return redirect('/end')
    
    if (len(answers) != qid):
        flash("Please answer the questions in order.")
        return redirect(f'/questions/{len(answers)}')
    
    question = satisfaction_survey.questions[qid]
    return render_template('questions.html', question=question)

@app.route('/answer', methods=["POST"])
def handle_answer():
    """Post answer to 'server' and go to next question"""

    answer = request.form['answer']

    answers = session['answers']
    answers.append(answer)
    session['answers'] = answers

    if (len(answers) == len(satisfaction_survey.questions)):
        return redirect('/end')
    
    return redirect(f'/questions/{len(answers)}')

@app.route('/end')
def finish_survey():
    """End the survey"""

    answers = session['answers']

    if (answers == None):
        flash("Please start the survey!")
        return redirect('/')
    if (len(answers) != len(satisfaction_survey.questions)):
        flash("Please finish the survey!")
        return redirect(f'/questions/{len(answers)}')
    
    results = dict(zip(satisfaction_survey.questions, answers))
    
    return render_template('end.html', results=results)