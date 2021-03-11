"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route("/")
def index_page():
    return render_template("cupcakes.html")

@app.route("/api/cupcakes")
def get_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]   
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_id(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
