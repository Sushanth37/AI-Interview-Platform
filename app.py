from flask import Flask, render_template, request
from resume_parser import extract_text
from ai_analyzer import analyze_resume
from question_generator import generate_questions
from mock_interview import evaluate_answer
from interview_report import generate_report
from database import cursor, db
import os

resume_data = ""

interview_questions = []

user_answers = []

current_index = 0

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload():

    global resume_data

    file = request.files["resume"]

    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(path)

    resume_text = extract_text(path)

    resume_data = resume_text

    analysis = analyze_resume(resume_text)

    return render_template(
        "analysis.html",
        analysis=analysis
    )
@app.route("/questions")
def questions():

    global resume_data
    global interview_questions

    questions_text = generate_questions(
        resume_data
    )

    interview_questions = [
        q.strip()
        for q in questions_text.split("\n")
        if q.strip()
    ]

    return render_template(
        "questions.html",
        questions=questions_text
    )
@app.route("/start_mock")
def start_mock():

    global current_index
    global user_answers

    current_index = 0
    user_answers = []

    return render_template(
        "interview.html",
        question=interview_questions[current_index],
        number=current_index + 1
    )
@app.route("/next_question", methods=["POST"])
def next_question():

    global current_index
    global user_answers
    global interview_questions

    answer = request.form["answer"]

    user_answers.append(answer)

    current_index += 1

    if current_index >= len(interview_questions):

        report = generate_report(
            interview_questions,
            user_answers
        )

        query = """
        INSERT INTO interview_history
        (
        score,
        technical_score,
        communication_score,
        confidence_score,
        feedback
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (
        "80",
        "8/10",
        "7/10",
        "8/10",
        report
        )

        cursor.execute(query, values)

        db.commit()

        return render_template(
            "evaluation.html",
            feedback=report,
            overall="80",
            technical="8/10",
            communication="7/10",
            confidence="8/10"
        )
    return render_template(
        "interview.html",
        question=interview_questions[current_index],
        number=current_index + 1
    )
@app.route("/dashboard")
def dashboard():

    cursor.execute(
        """
        SELECT *
        FROM interview_history
        ORDER BY created_at DESC
        """
    )

    records = cursor.fetchall()

    return render_template(
        "dashboard.html",
        records=records
    )
@app.route("/report/<int:id>")
def report(id):

    cursor.execute(
        """
        SELECT *
        FROM interview_history
        WHERE id=%s
        """,
        (id,)
    )

    record = cursor.fetchone()

    return render_template(
        "report.html",
        record=record
    )

if __name__ == "__main__":
    app.run(debug=True)