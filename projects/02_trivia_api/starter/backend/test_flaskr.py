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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:raghad@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)
        self.newquestion={"question":"new Q","answer":"nothing","difficulty":2,"category":5}
        self.searchTerm1={"searchTerm":"cat"}
        self.searchTerm2={"searchTerm":"ok"}
        self.preque_qucate={"previous_questions":[59,58,57,56,54,53],"quiz_category":{
		"type": "Geography",
		"id": 0
	}}
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
    def test_get_showcategory(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['categories'])
    def test_get_question(self):
        res=self.client().get('/questions')
        data=json.loads(res.data) 
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])  
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentCategory'])
    def test_get_question_notgoundpage(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'The server can not find the requested page.')
    def test_delete_question(self):
        res=self.client().delete('/questions/80')
        data=json.loads(res.data) 
        resl=Question.query.filter(Question.id==80).first()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True) 
        self.assertEqual(resl,None)
    def test_delete_question_notexist(self):
        res=self.client().delete('/questions/1000')
        data=json.loads(res.data) 
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'The server can not find the requested page.')
    def test_post_question(self):    
        res=self.client().post('/postquestion',json=self.newquestion)
        data=json.loads(res.data) 
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])  
        self.assertEqual(data['success'],True) 
    def test_search(self):
        res=self.client().get('/searshquestion',json=self.searchTerm1)
        data=json.loads(res.data) 
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])  
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
    def test_getQuestion_byCategory(self):
        res=self.client().get('/categories/5/questions?page=1')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])  
        self.assertTrue(data['totalQuestions']) 
        self.assertTrue(data['currentCategory'])  
    def test_getQuestion_byCategory_notfound(self):
        res=self.client().get('/categories/8/questions?page=1000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'The server can not find the requested page.') 
    def test_playquiz(self):
        res=self.client().get('/quizzes',json=self.preque_qucate)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200) 
        self.assertTrue(data['previousQuestions'])  
        self.assertTrue(data['question'])  

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()