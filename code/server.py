from flask import Flask;

app = Flask(__name__);

app.get("/")
app.get("/home")
def home():
    return