from flask import Blueprint, json, request, jsonify
from app.extensions import mongo
from datetime import datetime, timezone
import dateutil.parser

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def format_timestamp(iso_str):
    try:
        # Parse ISO string and ensure it's in UTC
        dt = dateutil.parser.isoparse(iso_str).astimezone(timezone.utc)
        # Format: 1st April 2021 - 9:30 PM UTC
        
        day = dt.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
            
        formatted_date = dt.strftime(f"{day}{suffix} %B %Y - %I:%M %p UTC")
        # remove leading zero from hours if any
        formatted_date = formatted_date.replace(" - 0", " - ")
        return formatted_date
    except Exception as e:
        return iso_str

@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event', '')
    
    if not payload:
        return jsonify({"status": "no payload"}), 400

    event_data = None
    
    if event_type == 'push':
        author = payload.get('pusher', {}).get('name', 'Unknown')
        ref = payload.get('ref', '')
        # ref is typically refs/heads/branch_name
        to_branch = ref.split('/')[-1] if '/' in ref else ref
        
        # Github push event timestamp from the repository updated_at or head_commit timestamp
        timestamp = payload.get('head_commit', {}).get('timestamp', datetime.utcnow().isoformat() + "Z")
        
        event_data = {
            "type": "PUSH",
            "author": author,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "formatted_timestamp": format_timestamp(timestamp),
            "created_at": datetime.utcnow()
        }
        
    elif event_type == 'pull_request':
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        author = pr.get('user', {}).get('login', 'Unknown')
        from_branch = pr.get('head', {}).get('ref', '')
        to_branch = pr.get('base', {}).get('ref', '')
        
        if action in ['opened', 'reopened']:
            timestamp = pr.get('created_at', datetime.utcnow().isoformat() + "Z")
            event_data = {
                "type": "PULL_REQUEST",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "formatted_timestamp": format_timestamp(timestamp),
                "created_at": datetime.utcnow()
            }
        elif action == 'closed' and pr.get('merged') == True:
            # Merged PR
            author = pr.get('merged_by', {}).get('login', author)
            timestamp = pr.get('merged_at', datetime.utcnow().isoformat() + "Z")
            event_data = {
                "type": "MERGE",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "formatted_timestamp": format_timestamp(timestamp),
                "created_at": datetime.utcnow()
            }
            
    if event_data:
        mongo.db.events.insert_one(event_data)
        return jsonify({"status": "success", "event": event_type}), 200
        
    return jsonify({"status": "ignored"}), 200

@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("created_at", -1).limit(50)
    result = []
    for event in events:
        event['_id'] = str(event['_id'])
        # clean up datetime for json dump
        if 'created_at' in event:
            event['created_at'] = event['created_at'].isoformat()
        result.append(event)
        
    return jsonify(result), 200
