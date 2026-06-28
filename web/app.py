from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    return jsonify()
    
@app.route("/stats", methods=["POST"])
def stats():
    return jsonify()
    