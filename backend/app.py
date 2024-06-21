from flask import Flask, render_template, request, jsonify
from requests import Response
from models import db, User
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uqgo0gix7xdyzbkl:DJzC7jFngX4rqFrX2pzH@bp174zjussxxr7thvuu1-mysql.services.clever-cloud.com:3306/bp174zjussxxr7thvuu1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json()
    user = User(**body)
    id=user.id
    db.session.add(user)
    db.session.commit()
    return {'id': str(id)},200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.as_dict()),200

@app.route('/users', methods=['GET'])
def get_users():
    usersRaw = User.query.all()
    users=[]
    for user in usersRaw:
        users.append(user.as_dict())
    resp = {
        "responseObject" : {
            "results":len(users),
            "users":users,
        }
    }
    return jsonify(resp),200


# @app.route('/users')
# def get_users():
    # # users = User
    # return Response(users, mimetype="application/json", status=200)
    # # return render_template('home.html')