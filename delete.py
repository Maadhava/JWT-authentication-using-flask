from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from crud import erase
app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os

delete_blueprint = Blueprint("delete", __name__, static_folder="static",
                template_folder="templates")

api_key=os.getenv('DELETE_API_KEY')
@delete_blueprint.route('/delete',methods=['DELETE'])
@jwt_required()
def delete():
    if request.headers["delete_key"]==api_key:
        token = get_jwt()
        email=token["sub"]
        erase(email)
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return jsonify(msg="delete success!")
    else:
        return "invalid api key!"
