import os
from flask import Flask, request, abort, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import json
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'

    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    '''
 @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def showcategory():
        data = Category.query.all()
        # create dict object to format the required  data structure in the
        # frontend
        formatted_categoris = {}
        for da in data:
            formatted_categoris.update({da.id: da.type})
        # the udacity's instructor way to format the dict
        # form_cate={d.id :d.type for d in data}
        return jsonify({"categories": formatted_categoris})
    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at
  the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def showquestion():
        data = Question.query.all()
        categories = Category.query.all()
        # format questions in a list as expected in the frontend
        formatted_questions = []
        for da in data:
            formatted_questions.append({"id": da.id,
                                        "question": da.question,
                                        "answer": da.answer,
                                        "category": da.category,
                                        "difficulty": da.difficulty})
        pagenum = request.args.get('page', 1, type=int)
        Start = (pagenum - 1) * QUESTIONS_PER_PAGE
        End = Start + QUESTIONS_PER_PAGE
        form_cate = {a.id: a.type for a in categories}
        if (len(formatted_questions[Start:End]) == 0):
            abort(404)
        return jsonify({'questions': formatted_questions[Start:End],
                        'totalQuestions': len(formatted_questions),
                        "categories": form_cate, "currentCategory": 1})
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.
  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def deletequestion(question_id):
        try:
            data = Question.query.get(question_id)
            data.delete()
            return jsonify({
                'success': True
            })
        except BaseException:
            abort(404)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  '''
    @app.route('/newquestion', methods=['POST', 'GET'])
    @cross_origin()
    def addquestion():
        question = request.get_json()['question']
        answer = request.get_json()['answer']
        difficulty = request.get_json()['difficulty']
        category = request.get_json()['category']
        formatted_questions = []

        try:
            newquestion = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty)
            newquestion.insert()
            allquestions = Question.query.order_by(Question.id).all()
            for da in allquestions:
                formatted_questions.append({"id": da.id,
                                            "question": da.question,
                                            "answer": da.answer,
                                            "category": da.category,
                                            "difficulty": da.difficulty})
            return jsonify({"questions": formatted_questions, "success": True})
        except BaseException:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/searshquestion', methods=['POST', 'GET'])
    @cross_origin()
    def searchquestion():
        searchterm = request.get_json()['searchTerm']
        formatted_questions = []

        # I used ilike to make the search case insensitive
        try:
            data = Question.query.filter(
                Question.question.ilike(f'%{searchterm}%')).all()
            for da in data:
                formatted_questions.append({"id": da.id,
                                            "question": da.question,
                                            "answer": da.answer,
                                            "category": da.category,
                                            "difficulty": da.difficulty})
            return jsonify({"questions": formatted_questions,
                            "totalQuestions": len(formatted_questions),
                            "currentCategory": 1
                            })
        except BaseException:
            abort(404)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.
  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @cross_origin()
    def showquestionBycategory(category_id):
        # stringify the category id because it's a string  in the questions
        # table in the database
        data = Question.query.filter(
            Question.category == str(category_id)).all()
        formatted_questions = []
        pagenum = request.args.get('page', 1, type=int)
        Start = (pagenum - 1) * 10
        End = Start + 10
        for da in data:
            formatted_questions.append({"id": da.id,
                                        "question": da.question,
                                        "answer": da.answer,
                                        "category": da.category,
                                        "difficulty": da.difficulty})
        if (len(formatted_questions[Start:End]) == 0):
            abort(404)
        return jsonify({"questions": formatted_questions[Start:End],
                        "totalQuestions": len(formatted_questions),
                        "currentCategory": category_id})
    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST', 'GET'])
    @cross_origin()
    def palyquiz():

        prev_ques = []
        allcategory_questions = []
        prev_ques = request.get_json()['previous_questions']
        category_id = request.get_json()['quiz_category']['id']
        if (category_id == 0):
            categoryQues = Question.query.all()
        else:
            categoryQues = Question.query.filter(
                Question.category == str(category_id)).all()
# -----------------------------------------------------------------------------
# this way display the questions as the same order in the database
# add the id in the list to prevent the repetition of questions
#  can't give range to generate random numbers,
# in questions table you may find that 34,2,67,35,76 questions' id in the
# same category therefore the question will be displayed in their order
# and then format the question as expected in the frontend
        for b in categoryQues:
            if (b.id not in prev_ques):
                prev_ques.append(b.id)
                return jsonify({
                    "question": b.format(), "previousQuestions": prev_ques
                })
        return jsonify({"success": True})
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The server can not find the requested page."
        }), 404

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unable to process the contained instructions"
        }), 422

    @app.errorhandler(403)
    def Forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access is forbidden to the requested page."
        }), 403

    @app.errorhandler(405)
    def MethodNotAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "The method specified in the request is not allowed."
        }), 405

    @app.errorhandler(500)
    def MethodNotAllowed(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error."
        }), 500

    @app.errorhandler(400)
    def MethodNotAllowed(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request."
        }), 400
    return app
