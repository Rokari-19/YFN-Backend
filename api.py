from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api, Resource, fields, reqparse, marshal_with, abort

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
api = Api(app)

    
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    
    def __repr__(self):
        return f"User(name = {self.name}), email = {self.email})"
# user args
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='This field is required')
user_args.add_argument('email', type=str, required=True, help='This field is required')

# for serializing data
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}
# class based requests, just like django views
class Users(Resource):
    
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
    
api.add_resource(Users, '/api/waitlist/')

@app.route('/api/waitlist/count/', methods=['GET'])
def get_waitlist_count():
    try:
        count = UserModel.query.count()
        return jsonify({'count': count}), 200
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)