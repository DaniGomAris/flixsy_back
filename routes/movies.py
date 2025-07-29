from flask import Blueprint, request, jsonify
from firebase_config import db

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/", methods=["GET"])
def get_movies():
    movies_ref = db.collection("movie")
    docs = movies_ref.stream()
    movies = [{**doc.to_dict(), "id": doc.id} for doc in docs]
    return jsonify(movies)


@movies_bp.route("/", methods=["POST"])
def add_movie():
    data = request.get_json()
    doc_ref = db.collection("movie").add(data)
    return jsonify({"message": "Movie added", "id": doc_ref[1].id}), 201


@movies_bp.route("/<movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        db.collection("movie").document(movie_id).delete()
        return jsonify({"message": "Movie deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@movies_bp.route("/<movie_id>", methods=["PUT"])
def update_movie(movie_id):
    data = request.get_json()
    try:
        db.collection("movie").document(movie_id).update(data)
        return jsonify({"message": "Movie updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500