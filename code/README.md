# How to run the project

### install all the dependencies first in the root directory:-

1. pip install flask (to install the main flask application) 
2. pip install flask-sqlalchemy (to install the orm communicating with sqlite database)
3. pip install flask-wtf (to install the flask version of wt_forms package)
4. pip install email-validator (to install the email validator required for the Email validtion in flask_wtforms package)
5. pip install flask-login (to install the login which is getting used in the project for authenticated)
6. pip install flask-bcrypt (to store the passwords in hashed form to keep our project safe during data breaches)
7. pip install python-dotenv (to install the dotenv package getting used in the project)

### Setup the dot-env file 

- SECRET_KEY=60f6e5c057dcb1e4cb8b4e0f907cb3b3d76422f00d38e3fa99c33d62ecae4871
- paste this secret key in the .env file that you would want to create in the folder named "A2Z_household_services" inside the current "code" folder
- and then most probably you're good to go 

### Run the server locally while making sure the location of the terminal is the "code folder"

- run this command for normal mode :- flask --app run.py run
- run this command for debug mode :- flask --app run.py run --debug
- in debug mode you can modify the code in certain lines of the folder from the browser itself 