from flask import Flask, request, render_template_string, redirect, url_for, jsonify, send_file
from chat import Chat
from image_generator import ImageGenerator
import os
import re

app = Flask(__name__)
chat = Chat(scenario_name="etherweave")  # Default to EtherWeave scenario
image_generator = ImageGenerator(cache_dir="image_cache")

# Simple form template for selecting or adding scenarios
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Alternative Internet</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        h1, h2 {
            color: #333;
        }
        .scenario-list {
            margin-bottom: 20px;
        }
        .scenario-item {
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #eee;
            border-radius: 3px;
        }
        .scenario-item:hover {
            background-color: #f9f9f9;
        }
        .scenario-name {
            font-weight: bold;
        }
        .scenario-desc {
            color: #666;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-size: 14px;
        }
        textarea {
            height: 120px;
        }
        button {
            background-color: #4285f4;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background-color: #3367d6;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #4285f4;
            text-decoration: none;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        .current-scenario {
            padding: 10px;
            background-color: #e8f0fe;
            border-radius: 3px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Alternative Internet Scenarios</h1>
        
        <div class="current-scenario">
            <p><strong>Current Scenario:</strong> {{ current_scenario }}</p>
            <a href="/" class="back-link">Browse Current Scenario</a>
        </div>
        
        <h2>Select a Scenario</h2>
        <div class="scenario-list">
            {% for scenario in scenarios %}
            <div class="scenario-item">
                <div class="scenario-name">{{ scenario.name }}</div>
                <div class="scenario-desc">{{ scenario.description }}</div>
                <form action="/select-scenario" method="post" style="margin-top: 10px;">
                    <input type="hidden" name="scenario_name" value="{{ scenario.name }}">
                    <button type="submit">Select This Scenario</button>
                </form>
            </div>
            {% endfor %}
        </div>
        
        <h2>Add Custom Scenario</h2>
        <form action="/add-scenario" method="post">
            <div class="form-group">
                <label for="name">Scenario Name:</label>
                <input type="text" id="name" name="name" required placeholder="e.g., steampunk">
            </div>
            <div class="form-group">
                <label for="description">Short Description:</label>
                <input type="text" id="description" name="description" required placeholder="e.g., Victorian-era steam-powered internet">
            </div>
            <div class="form-group">
                <label for="scenario">Full Scenario Description:</label>
                <textarea id="scenario" name="scenario" required placeholder="Describe your alternative internet in detail..."></textarea>
            </div>
            <button type="submit">Add Scenario</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Special case for the admin page
    if path == 'admin':
        scenarios = chat.get_available_scenarios()
        # Find the current scenario name based on the description
        current_scenario = next(
            (s["name"] for s in scenarios if chat.scenario_description.startswith(s["description"][:20])), 
            "Custom"
        )
        return render_template_string(
            TEMPLATE, 
            scenarios=scenarios,
            current_scenario=current_scenario
        )
    
    # Check if this is an image request (path ends with image extension)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if any(path.lower().endswith(ext) for ext in image_extensions):
        # Get image name and create prompt from it
        image_name = os.path.basename(path)
        prompt = image_generator.process_image_name(image_name)
        print(f"Generating image for: {prompt}")
        
        # Generate or retrieve image
        try:
            image_path = image_generator.get_or_generate_image(image_name)
            return send_file(image_path)
        except Exception as e:
            print(f"Error generating image: {e}")
            # If image generation fails, continue to normal page handling
        
    # Normal page handling
    html_content = chat.browse_to_page('/' + path)
    return html_content

@app.route('/add-scenario', methods=['POST'])
def add_scenario():
    name = request.form.get('name')
    description = request.form.get('description')
    scenario = request.form.get('scenario')
    
    if not all([name, description, scenario]):
        return "All fields are required", 400
    
    chat.add_custom_scenario(name, description, scenario)
    chat.change_scenario(scenario_name=name)
    
    return redirect('/admin')

@app.route('/select-scenario', methods=['POST'])
def select_scenario():
    scenario_name = request.form.get('scenario_name')
    if scenario_name:
        chat.change_scenario(scenario_name=scenario_name)
    
    return redirect('/admin')

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """API endpoint to get all available scenarios"""
    return jsonify(chat.get_available_scenarios())

@app.route('/api/scenarios/current', methods=['GET'])
def get_current_scenario():
    """API endpoint to get the current scenario"""
    scenarios = chat.get_available_scenarios()
    current_scenario = next(
        (s for s in scenarios if chat.scenario_description.startswith(s["description"][:20])), 
        {"name": "custom", "description": "Custom scenario"}
    )
    return jsonify(current_scenario)

@app.route('/api/scenarios/change', methods=['POST'])
def api_change_scenario():
    """API endpoint to change the current scenario"""
    data = request.json
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    scenario_name = data.get('name')
    if not scenario_name:
        return jsonify({"error": "Missing scenario name"}), 400
    
    success = chat.change_scenario(scenario_name=scenario_name)
    if success:
        return jsonify({"success": True, "message": f"Changed to scenario: {scenario_name}"})
    else:
        return jsonify({"success": False, "error": f"Scenario not found: {scenario_name}"}), 404
        

if __name__ == "__main__":
    app.run(debug=True, port=8080)
