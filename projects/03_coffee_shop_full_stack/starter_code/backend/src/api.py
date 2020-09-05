import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()
# ROUTES
# ------------------------------------------------------------------------------

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
     where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def drinks():
    try:
        thedrink = Drink.query.all()
        drinkforma = [d.long() for d in thedrink]
        return jsonify({"success": True, "drinks": drinkforma})
    except:
        abort(422)
# ------------------------------------------------------------------------------


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
     where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks(payload):
    try:
        thedrink = Drink.query.all()
        drinkforma = [d.long() for d in thedrink]
        return jsonify({"success": True, "drinks": drinkforma})
    except:
        abort(422)
# ------------------------------------------------------------------------------


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(payload):

    title = request.get_json()['title']
    recipe = request.get_json()['recipe']
    try:
        drink = Drink(title=title,   recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({'success': True, 'drinks': drink.long()})
    except:
        abort(422)

# ..........................................................................................


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, drink_id):
    all_drinks = Drink.query.all()
    #  one or none did not work for me so i came up with this way
    #  flag set to false unless i found matxh id, and is so then set the flasg
    # to true otherwise abort 404 error
    flag = False
    for da in all_drinks:
        if drink_id == da.id:
            flag = True
    if not flag:
        abort(404)
    if flag:
        try:
            thedata = request.get_json()
            thedrink = Drink.query.get(drink_id)
            if 'title' in thedata:
                thedrink.title = thedata.get('title', thedrink.title)
            if 'recipe' in thedata:
                thedrink.recipe = json.dumps(
                    thedata.get('recipe', thedrink.recipe))
            thedrink.update()
            return jsonify({'success': True, 'drinks': [thedrink.long()]})

        except:

            abort(422)


# ------------------------------------------------------------------------------
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
     where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    all_drinks = Drink.query.all()
    flag = False
    for da in all_drinks:
        if drink_id == da.id:
            flag = True
    if not flag:
        abort(404)
    if flag:
        try:
            thedrink = Drink.query.get(drink_id)
            if thedrink:
                thedrink.delete()
            return jsonify({"success": True, "delete": drink_id})
        except:
            abort(422)
# ------------------------------------------------------------------------------


# Error Handling
'''
Example error handling for unprocessable entity
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(403)
def Forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Access is forbidden to the requested page."
    }), 403


@app.errorhandler(500)
def InternalError(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error."
    }), 500


@app.errorhandler(400)
def BadRequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request."
    }), 400


'''

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "The server can not find the requested page."
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
