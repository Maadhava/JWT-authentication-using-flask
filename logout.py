from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import unset_jwt_cookies
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
logout_blueprint = Blueprint("logout", __name__, static_folder="static",
                template_folder="templates")

api_key=os.getenv('LOGOUT_API_KEY')

@logout_blueprint.route('/logout',methods=['POST'])
def logout():
    if request.headers["logout_key"]==api_key:
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response
