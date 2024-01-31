from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
responses_key="responses"

app=Flask(__name__)
app.config['SECRET_KEY']='ABC'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

@app.route('/')
def show_start_page():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    session[responses_key]=[]
    return redirect("questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):
    if qid != len(session.get(responses_key,[])):
        flash("Invalid question id. Redirecting to the current question")
        return redirect(f"/questions/{len(session.get(responses_key,[]))}")
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer_value=request.form.get('answer')

    responses=session[responses_key]
    responses.append(answer_value)
    session[responses_key]=responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')





