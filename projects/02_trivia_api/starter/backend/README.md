# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/category_id/questions'
POST '/searshquestion' 
POST '/postquestion'
POST '/quizzes'
DELETE '/questions/question_id'



GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
- Get all the questions from all categories and display 10 questions in each page 
- Request Arguments: None
- Returns: a question list that contains all the questions as an object in form of object.id.
"questions": [
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 2,
      "question": "What boxer original name is Cassius Clay?"
    }]
 totalQuestions return the number of all the questions from all categories.
 categories return the categories, which contains an object of id: category_string key: value pairs. 
 currentCategory: return the current category, default is none or one.

```
 DELETE '/questions/question_id'
 -Delete the question based on the given id 
 -Request Arguments: Question id 
 -Returns: JSON object to indicate the success of deletion
 

 POST '/postquestion'
 Add a question to the database from the user 
-Request Arguments: JSON object that contains the question, answer and both are strings, an integer to indicates the difficulty of the question, and the id of the category
-Returns: JSON that returns all the questions with the new question, and status that indicates the success of the post request
 {
      "answer": "the test",
      "category": "5",
      "difficulty": 3,
      "id": 19,
      "question": "new ques"
    }
  ],
  "success": true


POST '/searshquestion' 
search in all the questions to find a match question with the givin string 
-Request Arguments: JSON that contain the search term
-Returns: JSON object that contain the questions taht matches the search string, and totalQuestions give the nuber of questions taht were found,currentCategory return the current category the user in


GET '/categories/category_id/questions'
Display questions based on the given category
-Request Arguments: an integer that represents the id of the category
-Returns: JSON that contains questions list with 10 questions for each page, totalquestions is the number of questions in this category, currentcategory return the id of the current category

POST '/quizzes'
 To start playing a quiz by choosing a category or all the categories  and it will return a random question from a given category
 -Request Arguments:previous_questions list that has all the previous question to prevent repeating the question,quiz_category the id of the selected category to give question-based on the category
 -Returns: JSON that contains currentquestion is a single random question on the format of 
 "currentQuestion": {
    "answer": "tset",
    "category": "3",
    "difficulty": 4,
    "id": 10,
    "question": "test"
  }
 , previousQuestions return the previous question after adding the new one in the list 
  "previousQuestions": [
    59,
    9,
    57,
    11,
    54,
    13,
    10
  ]

Error Handling 
-The errors weil be return as JSON in this Format 
{  "success": False, 
   "error": 404,
   "message": "The server can not find the requested page."
}
4 types of errors will be handeld 
 -404 :Not Found
 -422 :Unprocessable
 -403 :Forbidden
 -405 :Method Not Allowed

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```