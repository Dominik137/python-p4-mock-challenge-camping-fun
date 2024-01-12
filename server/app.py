#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=["GET", "POST"])
def campers():
    campers = Camper.query.all()
    campers_list = []
    try:
        if request.method == "GET":
            for camper in campers:
                campers_list.append(camper.to_dict())
            return campers_list
    except:
        raise ValueError({"error": "Camper not found"})
    try:
        if request.method == "POST":
            json_dict = request.get_json()
        new_camper = Camper(
            name = json_dict.get("name"),
            age = json_dict.get("age")
        )
        db.session.add(new_camper)
        db.session.commit()
        # this adds it to our table
        return new_camper.to_dict(),201
    except:
        raise ValueError({ "errors": ["validation errors"] })
    
@app.route('/campers/<int:id>', methods=["GET", "PATCH"])
def camper_by_id(id):
    camper = Camper.query.filter_by(id=id).first()
    try:
        if request.method == "GET":
            return camper.to_dict()
    except:
        raise ValueError({"error": "Camper not found"})
    try:
        if request.method == "PATCH":
            json_dict = request.get_json()
            for attr in json_dict:
                setattr(camper, attr, json_dict.get(attr))
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict()
    except:
        raise ValueError({"validation errors"})

@app.route('/activities', methods=["GET"])
def activities():
    activities = Activity.query.all()
    activities_list = []
    try:
        if request.method == "GET":
            for activity in activities:
                activities_list.append(activity.to_dict())
            return activities_list
    except:
        raise ValueError({"error": "Activity not found"})

@app.route('/activities/<int:id>', methods=["DELETE"])
def activity_by_id(id):
    activity = Activity.query.filter_by(id=id).first()
    try:
        if id == id and request.method == "DELETE":
            db.session.delete(activity)
            db.session.commit()
            return "", 200
    except: raise ValueError({"error": "Activity not found"})

@app.route('/signups', methods=["POST"])
def singups():
    try:
        if request.method == "POST":
            json_dict = request.get_json()
        new_signup = Signup(
            camper_id = json_dict.get("camper_id"),
            activity_id = json_dict.get("activity_id"),
            time = json_dict.get("time")
        )
        db.session.add(new_signup)
        db.session.commit()
        # this adds it to our table
        return new_signup.to_dict(),201
    except:
        raise ValueError({ "errors": ["validation errors"] })



if __name__ == '__main__':
    app.run(port=5556, debug=True)
