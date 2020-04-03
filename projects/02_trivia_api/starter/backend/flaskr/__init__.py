import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#method to paginate questions
def pagination(request, question_lists):
  page = request.args.get("page", 1,type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  question_list = [question.format() for question in question_lists]
  return question_list[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)
    show_categories = [category.format() for category in categories]

    return jsonify({
      "success": True,
      "categories" : show_categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    num_of_question = len(questions)
    questions_for_page = pagination(request, questions)
    if len(questions_for_page) == 0:
      abort(404)
    categories = Category.query.order_by(Category.id).all()
    show_categories = [category.format() for category in categories]
    return jsonify({
      "success": True,
      "questions" : questions_for_page,
      'total_questions' : num_of_question,
      "categories" : show_categories
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''



  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id ==question_id).one_or_none()
      if question is None:
        abort(404)
      else:
        question.delete()
      return jsonify({
        "success": True,
        "delete": question_id
      })
    except:
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
  @app.route('/questions', methods = ['POST'])
  def post_question():
    body = request.get_json()
    search = body.get('searchTerm')
    if(search):
      search = "%" + search +"%"
      searchResult =  Question.query.filter(Question.question.ilike(search)).all()
      if(len(searchResult) == 0):
        abort(404)
      else:
        pagedResult = pagination(request, searchResult)
        return  jsonify({
          'success' : True,
          'question' : pagedResult,
          'total_questions': len(Question.query.all())
        })
    else:
      question = body.get('question')
      answer = body.get('answer')
      difficulty = body.get('difficulty')
      category = body.get('category')
      if ((question is None) or (answer is None) or (difficulty is None) or (category is None)):
        abort(422)
      try:
        question = Question(
          question = question,
          answer = answer,
          difficulty = difficulty,
          category = category
        )
        question.insert()
        questions =  Question.query.all()
        pagedQuestions = pagination(request, questions)
        return jsonify({
          'success' : True,
          'created' : question.id,
          'question_created': question.question,
          'questions': pagedQuestions,
          'total_questions': len(Question.query.all())

        })
      except:
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

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_categories(id):
    category = Category.query.filter_by(id = id).one_or_none()
    if category is None:
      abort(404)
    question_list = Question.query.filter_by(category= category.id).all()
    pagedQuestionList = pagination(request,question_list)
    if len(pagedQuestionList) ==0:
      abort(404)
    return jsonify({
      "success" : True,
      "questions" : pagedQuestionList,
      'total_questions': len(Question.query.all()),
      'current_category': category.type
    })

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

  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()
    quiz_category = body.get('quiz_category')
    previous_questions = body.get('previous_questions')
    if ((quiz_category is None) or (previous_questions is None)):
      abort(400)
    if(quiz_category['id'] == 0):
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=quiz_category['id']).all()
    question = questions[random.randrange(0, len(questions), 1)]


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
      "message": "Page not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "not valid operation"
    }), 422


  return app

    