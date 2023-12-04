from flask import Flask, render_template, request, flash, redirect, session, make_response
from surveys import surveys

app =Flask(__name__)
app.config['SECRET_KEY'] = "secret-key"

Curr_Sur_Key = 'current_survey'
Responses_Key = "responses"

@app.route("/")
def home_page():
    """Renders list of surveys to pick from"""
    return render_template('survey-selector.html', surveys = surveys)

@app.route("/survey-writeup", methods=['post'])
def survey_info():
    """Renders title and instrutions"""

    svy_id = request.form['selected-survey']
    survey = surveys[svy_id]
    session[Curr_Sur_Key] = svy_id
    session[Responses_Key] = []
    
    if request.cookies.get(f"completed_{svy_id}"):
       return redirect("/completed")

    return render_template('start-survey.html', survey = survey)

@app.route("/questions/<int:qid>", methods=["post","get"])
def question_page(qid):

    responses = session.get(Responses_Key)
    survey_key = session[Curr_Sur_Key]
    survey = surveys[survey_key]
    question = survey.questions[qid]

    if (len(responses) == len(survey.questions)):
        return redirect("/completed")
    if (len(responses) != qid):
        flash("Please no skipping ahead. Thank you.")
        return redirect(f"/questions/{len(responses)}")
    
    return render_template("questions.html", num = qid, question = question)

@app.route('/answer', methods=["post"])
def answer_question():
    answer = request.form["answer"]

    responses = session[Responses_Key]
    responses.append(answer)
    session[Responses_Key] = responses

    survey_key = session[Curr_Sur_Key]
    survey = surveys[survey_key]

    if (len(responses) == len(survey.questions)):
        return redirect("/completed")
    else:
        return redirect(f"/questions/{len(responses)}")  
    
@app.route("/completed")
def completed_survey():
    survey_key = session[Curr_Sur_Key]
    survey = surveys[survey_key]

    HTML = render_template('completed.html', survey = survey)
    res = make_response(HTML)
    res.set_cookie(f"completed_{survey_key}", "yes", max_age=30)
    return res