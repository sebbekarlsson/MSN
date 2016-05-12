from flask import Flask, request, jsonify, session
from server.models import User
from server.mongo import db
from server.utils import id_generator
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = 'dot123123'

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = db.collections.find_one({
            'structure': '#User',
            'email': email
        })

    if existing_user is None:
        return jsonify({'response': {'text': 'User does not exist.'}})

    if password != existing_user['password']:
        return jsonify({'response': {'text': 'Wrong password.'}})
    
    token = id_generator()
    db.collections.update(
            {'structure': '#User', '_id': existing_user['_id']},
            {'$set' : {'token': token}}
            )
    
    session['user_id'] = str(existing_user['_id'])
    return jsonify(
            {
                'response': {
                    'text': 'OK',
                    'token': token,
                    'user_id': str(existing_user['_id'])
                    }
                }
            )

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    
    try:
        if len(email) < 3:
            return jsonify({'response': {'text': 'Email is not valid.'}})
        if len(password) < 3:
            return jsonify({'response': {'text': 'Password is not valid.'}})
        if len(firstname) < 3:
            return jsonify({'response': {'text': 'Firstname is not valid.'}})
        if len(lastname) < 3:
            return jsonify({'response': {'text': 'Lastname is not valid.'}})
    except TypeError:
        return jsonify({'response': {'text': 'One or many fields are missing.'}})

    existing_user = db.collections.find_one({
            'structure': '#User',
            'email': email
        })

    print(existing_user)

    if existing_user is not None:
        return jsonify({'response': {'text': 'This user is already registered.'}})
    else:
        user  = User(
                    email=email,
                    password=password,
                    firstname=firstname,
                    lastname=lastname
                )
        db.collections.insert_one(user.export())
        return jsonify({'response': {'text': 'OK'}})


@app.route('/user', defaults={'user_id': None})
@app.route('/user/<user_id>')
def get_user(user_id):
    if user_id is None:
        user_id = sesion['user_id']

    user = db.collections.find_one({'structure': '#User', '_id': ObjectId(user_id)})
    contacts = []
    
    for contact in user['contacts']:
        contacts.append(str(contact))

    if user is not None:
        return jsonify({'firstname': user['firstname'], 'contacts': contacts, 'user_id': user_id})
    else:
        return jsonify({'user': 'None'})

if __name__ == '__main__':
    app.run(debug=True)
