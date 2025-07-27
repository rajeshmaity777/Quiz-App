
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random

app = Flask(__name__)

with open("quiz_data.json", "r") as file:
    quiz_data = json.load(file)

@app.route("/")
def index():
   
    random_questions = random.sample(quiz_data, 10)
    return render_template("index.html", questions=random_questions)

@app.route("/submit", methods=["POST"])
def submit():
    user_answers = request.form
    score = 0
    correct_answers = {q["id"]: q["answer"] for q in quiz_data}

    analysis = []
    incorrect_questions = []
    for q_id, user_answer in user_answers.items():
        correct_answer = correct_answers.get(q_id, None)
        question_text = next((q["question"] for q in quiz_data if q["id"] == q_id), "Unknown question")
        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
        else:
            incorrect_questions.append(question_text)
        analysis.append({
            "question": question_text,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
        })
    total_questions = len(user_answers)
    accuracy = (score / total_questions) * 100 if total_questions > 0 else 0
    skill_gap = "Great job! No gaps detected." if not incorrect_questions else f"Review the following questions: {', '.join(incorrect_questions)}"

    return render_template(
        "result.html",
        score=score,
        total=total_questions,
        analysis=analysis,
        accuracy=accuracy,
        skill_gap=skill_gap,
    )

if __name__ == "__main__":
    app.run(debug=True)
