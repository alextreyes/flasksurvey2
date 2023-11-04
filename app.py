from flask import Flask, request, render_template, session, redirect, flash 
from surveys import satisfaction_survey as survey



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

responses =[]
@app.route("/")
def show_home():
    title = survey.title
    return render_template("home.html", title=title)


@app.route("/questions/<int:question_number>")
def show_question(question_number):
    responses = session.get('responses')
    question_list = survey.questions
    

    if responses is None :
        flash('No questions responded')
        return redirect("/")
    if len(responses) == len(survey.questions):
        return redirect("/complete")
    if len(responses) != question_number:
        flash("don't skip")
        return redirect(f'/questions/{len(responses)}')
    if question_number > len(survey.questions):
        flash("out of range, don't skip")
        return redirect(f'/questions/{len(responses)}')
    question = question_list[question_number]

    return render_template("question.html", question_list=question_list, question_number=question_number, question=question)

@app.route("/start", methods=["POST"])
def start():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def add_to_list():
    

    answer = request.form["answer"]
    responses.append(answer)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():   
    return render_template("complete.html")




