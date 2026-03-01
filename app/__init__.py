from flask import Flask, render_template
from app.webhook.routes import webhook
from app.extensions import mongo

def create_app():
    app = Flask(__name__)
    
    # Configure MongoDB URI
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    
    # Initialize extensions
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(webhook)
    
    @app.route('/', methods=["GET"])
    def index():
        return render_template('index.html')
        
    return app
