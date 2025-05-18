from flask import Flask, request, abort, render_template_string, redirect
import secrets
import time

app = Flask(__name__)
links = {}  # token: expiry

@app.route('/')
def root():
    return abort(403)

@app.route('/generate', methods=['GET'])
def generate():
    token = secrets.token_urlsafe(8)
    links[token] = time.time() + 120  # valid for 2 minutes
    return redirect(f'/server?={token}')

@app.route('/server')
def serve():
    token = request.args.get('')
    current_time = time.time()

    if token is None:
        return abort(403)
    
    if token in links:
        if current_time <= links[token]:
            with open("index.html", "r") as f:
                html = f.read().replace("{{token}}", token)
            return render_template_string(html)
        else:
            return open("404.html").read(), 404
    else:
        return abort(403)

@app.route('/exit')
def exit_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
        return "Server Closed!"
    return "Cannot shut down."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
