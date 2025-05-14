from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from models import ThoughtModel
from extensions import db
from datetime import datetime, UTC

api = Namespace("thoughts", description="Gestione thoughts")

thought_model = api.model("Thought", {
    "id": fields.Integer,
    "username": fields.String,
    "text": fields.String,
    "timestamp": fields.DateTime
})

parser = reqparse.RequestParser()
parser.add_argument("username", required=True, help="Usarname obbligatorio")
parser.add_argument("text", required=True, help="Testo obbligatorio")

def validate_token(token):
    return token == "Bearer valid-token"


@api.route("/")
class ThoughList(Resource):

    @api.marshal_list_with(thought_model)
    def get(self):
        return ThoughtModel.query.all()
    
    @api.marshal_list_with(thought_model)
    def post(self):
        token = request.headers.get("Authorization")
        if not validate_token(token):
            api.abort(401, "Token non valido")

        args = parser.parse_args()
        new_thought = ThoughtModel(
            username=args["username"],
            text=args["text"],
            timestamp=datetime.now(UTC))
        
        db.session.add(new_thought)
        db.session.commit()
        return new_thought, 201
    

@api.route("/<int:id>")
class Thought(Resource):
    @api.marshal_with(thought_model)
    def get(self, id):
        thought = db.session.get(ThoughtModel, id)
        if not thought:
            api.abort(404, "Thought non trovato")
        return thought
    
    