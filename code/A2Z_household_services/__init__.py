import os;
from flask import Flask; # type: ignore
from flask_sqlalchemy import SQLAlchemy;
from flask_bcrypt import Bcrypt; # type: ignore
from flask_login import LoginManager; # type: ignore
from dotenv import load_dotenv; # type: ignore

load_dotenv()

app = Flask(__name__, template_folder='./templates', static_folder='./static')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///A2Zdatabase.db";

app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app);

flask_bcrypt_instance = Bcrypt(app);

login_manager = LoginManager();
login_manager.init_app(app);
login_manager.login_view = 'login';
login_manager.login_message_category = 'info';

from A2Z_household_services import routes;