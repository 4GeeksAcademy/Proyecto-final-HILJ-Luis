"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@app.route('/tags', methods=['POST'])
def create_tag():
    name = request.json['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({'message': 'Tag created successfully!'}), 201

@app.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{'id': tag.id, 'name': tag.name} for tag in tags])

@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    name = request.json['name']
    tag_ids = request.json.get('tag_ids', [])
    itinerary = Itinerary(name=name)
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    itinerary.tags.extend(tags)
    db.session.add(itinerary)
    db.session.commit()
    return jsonify({'message': 'Itinerary created successfully!'}), 201

@app.route('/itineraries', methods=['GET'])
def get_itineraries():
    itineraries = Itinerary.query.all()
    data = []
    for itinerary in itineraries:
        tags = [{'id': tag.id, 'name': tag.name} for tag in itinerary.tags]
        data.append({'id': itinerary.id, 'name': itinerary.name, 'tags': tags})
    return jsonify(data)

