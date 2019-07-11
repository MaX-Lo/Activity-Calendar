import json
import logging
import os
from typing import Optional, List

from flask import Flask, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_DIR = './data'
ACTIVITIES_FN = "activities.json"
CATEGORIES_FN = "categories.json"

logging.getLogger('flask_cors').level = logging.DEBUG


def save(file_name: str, data: str):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    with open(f'{DATA_DIR}/{file_name}', 'w') as f:
        f.write(data)


def read(file_name: str) -> Optional[str]:
    if not os.path.exists(f'{DATA_DIR}/{file_name}'):
        return

    with open(f'{DATA_DIR}/{file_name}', 'r') as f:
        return ''.join(f.readlines())


def load_categories() -> List:
    categories_str = read(CATEGORIES_FN)
    if not categories_str:
        categories_str = '[]'
    return json.loads(categories_str)


def load_activities() -> List:
    activities_str = read(ACTIVITIES_FN)
    if not activities_str:
        activities_str = '[]'
    return json.loads(activities_str)


activities = load_activities()
categories = load_categories()


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
        print(categories)
        return json.dumps(categories)


def add_category(name: str, description: str, color: str):
    category = {"name": name, "description:": description, "color": color}
    categories.append(category)
    save(CATEGORIES_FN, json.dumps(categories))
    return category


def add_activity(category: str, date: str):
    activity = {"category": category, "date": date}
    activities.append(activity)
    save(ACTIVITIES_FN, json.dumps(activities))
    return activity
