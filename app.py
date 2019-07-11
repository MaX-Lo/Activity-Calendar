import json
from typing import List, Dict

from flask import Flask, request, send_from_directory
from flask_cors import CORS

import file_handler as fh

app = Flask(__name__)
CORS(app)


activities = fh.load_activities()
categories = fh.load_categories()


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/')
def root_request():
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def static_file_request(path):
    return send_from_directory('static', path)


@app.route('/activities', methods=['GET', 'POST'])
def activities_route():
    if request.method == 'POST':
        return add_activity(request.json['category'], request.json['date'])

    if request.method == 'GET':
        return json.dumps(activities)


@app.route('/categories', methods=['GET', 'POST'])
def categories_route():
    if request.method == 'POST':
        color = request.json['color'] if ('color' in request.json) else "100, 240, 100"
        return add_category(request.json['name'], request.json['description'], color)

    if request.method == 'GET':
        return json.dumps(categories)


@app.route('/activities/<category>')
def get_activities_by_category(category: str) -> List[Dict]:
    global activities
    activities_for_category = list(filter(lambda activity: activity['category'] == category, activities))
    return json.dumps(activities_for_category)


def add_category(name: str, description: str, color: str):
    category = {"name": name, "description:": description, "color": color}
    categories.append(category)
    fh.save(fh.CATEGORIES_FN, json.dumps(categories))
    return category


def add_activity(category: str, date: str):
    activity = {"category": category, "date": date}
    activities.append(activity)
    fh.save(fh.ACTIVITIES_FN, json.dumps(activities))
    return activity
