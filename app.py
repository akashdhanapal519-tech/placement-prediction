from flask import Flask, render_template, redirect, url_for, session
from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
import threading

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

def train_model_background():
    """Train ML model in background on startup"""
    try:
        from ml.train import train_model
        train_model()
        print("[APP] ML model ready!")
    except Exception as ex:
        print(f"[APP] ML training error: {ex}")

if __name__ == '__main__':
    init_db()
    # Train model in background thread so server starts fast
    t = threading.Thread(target=train_model_background, daemon=True)
    t.start()
    print("=" * 55)
    print("  Student Placement Prediction System")
    print("  URL: http://127.0.0.1:5000")
    print("  Admin: admin / admin123")
    print("=" * 55)
    app.run(debug=True, use_reloader=False, port=5000)
