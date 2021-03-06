*User Authentication using JWT:

A Rest API using python which handles user authentication.
The user authentication needs to have these options:-
  1. Sign Up
  2. Sign In
  3. Forgot password aka (/send-mail/)
  4. Logout
  5. Delete
  6. Dashboard
Task is implemented using JWT. To perform operation after login/ Register, request is sent containing JWT only to the server. @app.after_request callback used for refreshing the token. For each request token will refresh.
1. SignUp
    To create user details(User ID, Password, Email ID) and add to database.
    JWT_acess_token generated.

    '''json
    Data to be sent:
    Sign up:
    {
        "Username": " ABC", 
        "Email": " Abc@gmail.com", 
        "Password": " 1234"
    }

    If the credentials are correct returns "user created!"
    else returns "invalid credentials!"
    '''




2. SignIn
    Enter the user credentials and login to site.
    JWT_access_token generated.
    If user is inactive for more than 10 mins, needs to Re-LogIn.
    same as signup works only if all the credentials are correct.
    
    Data to be sent:
    '''json
    {
        "Email": " Abc@gmail.com", 
        "Password": " 1234"
    }
    Data to be recieved:
    If the credentials are correct access token will be generated and it will return "login successful!" else returns "invalid credentials!"
    '''


3. Forgot password(/send-mail/)
    To generate random 4 digit code to user's Mail ID sent by the Server and the password is updated in the database.
    '''json
    Data sent:
    {
        "email":"abc@gmail.com"
    }

    Data recieved:
    an autogenerated password will be updated in the database and sent back to the user.
    '''


4. LogOut
    To exit and expire the JWT_access_token.
    nothing is sent to the backend and the tokens which are set in the cookies are unset.


5. Delete
    since email is the only column which isn't redundant deletion is done using email
    '''json
    data sent:
    {
        "email":"abc@gmail.com"
    }
    
    data recieved:
    {
        msg="delete successful!"
    }
    '''
    To remove the user credentials from the database.

6. Dashboard
    This route can be accessed only with a valid token


NOTE:
JWT's are stored in cookies and set with an expiry of 10 minutes and if the user is inactive more than 10 mins needs to relogin else the expiry is postponed accordingly.


ARCHITECTURE:
    Programming Language: Flask
    Database: PostgreSQL


Connecting postgres:

In python postgres can be simply connected using an adapter psycopg2.
Install postgres from https://www.postgresql.org/download/windows/

conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host='localhost'):this just does the  establishing connection.
the above statement returns a connection object which is essential for querying.


to create a database:
*open pgadmin4
*start the server
*click Object->Create->Database->give the name and save
  

creating the table and quering is similar to sqlite3.


Installing virtualenv:

open command prompt:
pip install virtualenv
python -m venv venv_name
venv_name\Scripts\activate.bat
 
NOTE:venv refers to the virtUal environment name that u have given.