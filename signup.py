from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from datetime import timedelta
from crud import fetch,create
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
signup_blueprint = Blueprint("signup", __name__, static_folder="static",
                template_folder="templates")

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
jwt = JWTManager(app)


api_key=os.getenv('SIGNUP_API_KEY')

@signup_blueprint.route('/signup',methods=['POST'])
def signup():
    if request.headers["signup_key"]==api_key:
        username=request.json["username"]
        password=request.json["password"]
        email=request.json["email"]
        if username and password and email:
            if isinstance(username,str) and isinstance(password,str) and isinstance(email,str):
                res=fetch(email)
                if len(res)==0:
                    create(username,email,password)
                    response = jsonify({"msg": "user created!"},200)
                    access_token = create_access_token(identity=email)
                    set_access_cookies(response, access_token)
                    return response
                else:
                    return "user exists!"
            else:
                return jsonify(msg="invalid credentials")
        else:
            return jsonify(msg="invalid credentials")