import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('postgres:1234@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_404_get_paginated_questions_out_of_range(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    def test_delete_question(self):
        response = self.client().delete('/questions/27')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 27)

    def test_404_delete_question(self):
        response = self.client().delete('/questions/99999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_post_new_question(self):
        post_data = {
            'question': 'what is your name',
            'answer': 'Alice',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=post_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question_created"], 'what is your name')
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["created"])

    def test_422_post_new_question(self):
        post_data = {

        }
        response = self.client().post('/questions', json=post_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'not valid operation')

    def test_search_questions(self):
        post_data = {
            'searchTerm': 'a',
        }
        response = self.client().post('/questions', json=post_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["question"])


    def test_404_search_questions(self):
        post_data = {
            'searchTerm': 'abcdefghijklmnopqrst',
        }
        response = self.client().post('/questions', json=post_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_question_by_category(self):
        response = self.client().get('/categories/1/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["current_category"]))

    def test_404_question_by_category(self):
        response = self.client().get('/categories/1/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_play_quiz(self):
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        }
        response = self.client().post('/quizzes', json=post_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])

    def test_404_play_quiz(self):
        post_data = {

            }

        response = self.client().post('/quizzes', json=post_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Page not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()