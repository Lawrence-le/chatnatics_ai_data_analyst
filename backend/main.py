# app.py

# from config import create_app
# from flask_socketio import SocketIO
# import eventlet

# eventlet.monkey_patch()  # Patches standard library to be async-friendly

from app import create_app  # Import socketio from the app package


app = create_app()


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
