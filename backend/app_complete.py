from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
import os
import pdfkit

# Initialize app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database models
class FDInstalment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Schemas
class FDInstalmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FDInstalment

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

fd_schema = FDInstalmentSchema()
fd_list_schema = FDInstalmentSchema(many=True)
user_schema = UserSchema()

# Helper functions
def calculate_maturity(fd):
    maturity_amount = fd.amount * (1 + (fd.interest_rate / 100) * fd.tenure)
    return maturity_amount

# Authentication
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        access_token = create_access_token(identity={'username': username})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# FD Management
@app.route('/fd', methods=['POST'])
@jwt_required()
def create_fd():
    amount = request.json['amount']
    interest_rate = request.json['interest_rate']
    tenure = request.json['tenure']
    new_fd = FDInstalment(amount=amount, interest_rate=interest_rate, tenure=tenure)
    db.session.add(new_fd)
    db.session.commit()
    return fd_schema.jsonify(new_fd), 201

@app.route('/fd/<id>', methods=['GET'])
@jwt_required()
def get_fd(id):
    fd = FDInstalment.query.get(id)
    return fd_schema.jsonify(fd)

@app.route('/fd/<id>/maturity', methods=['GET'])
@jwt_required()
def fd_maturity(id):
    fd = FDInstalment.query.get(id)
    maturity_amount = calculate_maturity(fd)
    return jsonify({'maturity_amount': maturity_amount})

@app.route('/fd/<id>/premature', methods=['POST'])
@jwt_required()
def premature_closure(id):
    fd = FDInstalment.query.get(id)
    # Simulate premature closure logic
    closure_amount = fd.amount * 0.90  # assuming 10% penalty
    return jsonify({'closure_amount': closure_amount})

@app.route('/fd/<id>/receipt', methods=['GET'])
@jwt_required()
def generate_receipt(id):
    fd = FDInstalment.query.get(id)
    receipt_content = f'Deposit Amount: {fd.amount}\nInterest Rate: {fd.interest_rate}\nTenure: {fd.tenure} months\nMaturity Amount: {calculate_maturity(fd)}'
    pdf_output = pdfkit.from_string(receipt_content, False)
    return send_file(pdf_output, attachment_filename='receipt.pdf', as_attachment=True)

# Run server
if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)