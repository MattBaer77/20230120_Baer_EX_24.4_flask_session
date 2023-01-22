# First we must import Flask
# and by importing a flask object called request 
from flask import Flask, request, render_template, redirect, flash, session

# Importing surveys.py
from surveys import surveys

# Importing the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension

# This command initiates server - tells flask to do it's thing in the file.
app = Flask(__name__)

app.config['SECRET_KEY'] = "george_costanza"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)




current_survey = 'satisfaction'

@app.route('/')
def home_page():
    # survey_title = surveys.satisfaction_survey.title
    survey_title = surveys[current_survey].title

    # session['responses'] = []

    return render_template(
        'root.html',
        survey_title=survey_title,
        )


@app.route('/startsurvey', methods=['POST'])
def start_survey():
    session["responses"] = []

    return redirect('/questions/0')


@app.route('/questions/<int:questidx>')
def question(questidx):

    if (len(session["responses"]) != questidx):
        flash('A - Please answer the current question.')
        return redirect(f'/questions/{len(session["responses"])}')

    survey_question = surveys[current_survey].questions[questidx].question
    survey_choices = surveys[current_survey].questions[questidx].choices

    return render_template(
        'question_page.html',
        this_question=questidx,
        survey_choices=survey_choices,
        question=survey_question
        )


@app.route('/answer/<int:answeridx>', methods=['POST'])
def answer(answeridx):

    if request.form == {}:
        flash('B - Please answer the current question.')
        return redirect(f'/questions/{len(session["responses"])}')

    answer = request.form['options']

    response_list = session["responses"]


    if len(session["responses"]) == answeridx:
        response_list.append(answer)
        session["responses"] = response_list
    else:
        response_list[answeridx] = answer
        session["responses"] = response_list


    if len(session["responses"]) == len(surveys[current_survey].questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{len(session["responses"])}')


@app.route('/thankyou')
def thankyou():

    print(session["responses"])

    if len(session["responses"]) < len(surveys[current_survey].questions):
        flash('C - Please answer the current question')
        return redirect(f'/questions/{len(session["responses"])}')

    return render_template('thankyou.html')
