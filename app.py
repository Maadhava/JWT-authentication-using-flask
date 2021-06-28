from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask,request
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from signin import signin_blueprint
from signup import signup_blueprint
from logout import logout_blueprint
from delete import delete_blueprint
import os


app = Flask(__name__)
DB_NAME=os.getenv('DB_NAME')

DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
import psycopg2
conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host='localhost')
cursor=conn.cursor()
command1 = """CREATE TABLE IF NOT EXISTS
userdetails(username TEXT,email TEXT,password TEXT)"""
cursor.execute(command1)


from flask_mail import Mail, Message
import random



app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = str(os.getenv('secret_key'))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config["JWT_CSRF_IN_COOKIES"]=True
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME =os.getenv('email') ,
    MAIL_PASSWORD =os.getenv('password')
    )
mail = Mail(app)
jwt = JWTManager(app)
# DB_NAME=os.getenv('DB_NAME')

# DB_USER=os.getenv('DB_USER')
# DB_PASS=os.getenv('DB_PASS')
# import psycopg2
# conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host='localhost')
# cursor=conn.cursor()
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


app.register_blueprint(signin_blueprint, url_prefix="/")
app.register_blueprint(signup_blueprint, url_prefix="/")
app.register_blueprint(logout_blueprint, url_prefix="/")
app.register_blueprint(delete_blueprint, url_prefix="/")

@app.route("/dashboard")
@jwt_required()
def protected():
    return jsonify(msg="Now u are accessing a protected place!")

@app.route('/send-mail/')
def send_mail():
    e=None
    try:
        n = random.randint(0,9999)
        recipient=request.json["email"]
        msg = Message("Password:",
          sender=os.getenv('email'),
          recipients=[recipient])
        n=str(n)
        msg.body =n
        mail.send(msg)
        cursor.execute("update userdetails set password=(%s) where email=(%s)",(n,recipient))
        conn.commit()
        return 'Mail sent!'
    except Exception as e:
        return(str(e))

@app.route('/fetch')
def fetch():
    cursor.execute("select * from userdetails")
    res=cursor.fetchall()
    return jsonify(token=res)


if __name__ == "__main__":
    app.run(debug=True)