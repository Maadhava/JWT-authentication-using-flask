from flask import Flask, json,request,jsonify,Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from crud import check
app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os

signin_blueprint = Blueprint("signin", __name__, static_folder="static",
                template_folder="templates")

api_key=os.getenv('SIGNIN_API_KEY')

@signin_blueprint.route('/signin',methods=['POST'])
def signin():
    if request.headers["signin_key"]==api_key:
        username=request.json["username"]
        password=request.json["password"]
        email=request.json["email"]
        if username and password and email:
            if isinstance(username,str) and isinstance(password,str) and isinstance(email,str):
                res=check(username,email,password)
                if len(res)==1:
                    response = jsonify({"msg": "login successful"},200)
                    access_token = create_access_token(identity=email)
                    set_access_cookies(response, access_token)
                    return response
                else:
                    return jsonify({"msg":"Invalid user!"},401)
            else:
                return jsonify({"msg":"invalid credentials"},401)
        else:
            return jsonify({"msg":"invalid credentials"},401)
    else:
        return jsonify({"msg":"SERVER ERROR"},500)
