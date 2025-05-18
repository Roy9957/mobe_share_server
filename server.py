from flask import Flask, request, redirect, render_template, abort, url_for
import time
import uuid
import os

app = Flask(__name__)
valid_links = {}

@app.route("/")
def home():
    return abort(403)

@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        token = str(uuid.uuid4())[:12]
        valid_links[token] = time.time() + 300  # 5 মিনিটের জন্য ভ্যালিড
        return f"https://mobe-share-server.onrender.com/mobe_share?token={token}"
    return "Only POST allowed"

@app.route("/mobe_share")
def mobe_share():
    token = request.args.get("token")
    if token in valid_links:
        if time.time() < valid_links[token]:
            return render_template("index.html", token=token)
        else:
            del valid_links[token]
            return abort(404)
    return abort(404)

@app.route("/server")
def game_redirect():
    token = request.args.get("token")
    if token in valid_links and time.time() < valid_links[token]:
        return redirect("https://www.mobe-game.rf.gd/game.html")
    return abort(404)

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1000))
    app.run(host="0.0.0.0", port=port, debug=True)
