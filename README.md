# AlternativeInternet

A framework for generating fictional alternative internet experiences that explore how the web might have evolved under different technological and cultural scenarios.

## Overview

AlternativeInternet generates immersive fictional web experiences based on different technological and design scenarios. It uses language models to create content that simulates alternative internet histories and interfaces, from retrofuturist computing to mystical networks.

## Features

- **Multiple Fictional Scenarios**: Includes Retrofuturist, Etherweave, Cyberpunk, and Solarpunk scenarios
- **Dynamic Content Generation**: Creates realistic content using language models
- **Interactive Chat Interface**: Engage with the fictional internet through a chat-based interface
- **Image Generation**: Custom imagery that matches each alternative scenario
- **Extensible Framework**: Easy to add new fictional scenarios

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/username/AlternativeInternet.git
cd AlternativeInternet
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
CEREBRAS_API_KEY=your_cerebras_api_key  # If using Cerebras
FAL_KEY=your_fal_api_key                # For image generation
```

## Usage

### Run the main application
```bash
python main.py
```

This will start the web server on port 8080. Navigate to `http://localhost:8080` in your browser to view the application.

### Use the chat interface
```bash
python chat.py
```

### Navigation

The application dynamically generates pages based on the URL paths:

1. The main entry point is at the root URL (`/`), which shows the home page for the current scenario
2. All other URLs are handled by a catch-all route that generates content based on the path
3. Pages follow a typical web structure like `/tld/domain/page/subpage`
4. Links within pages direct to other pages within the same fictional internet scenario
5. The application handles image requests automatically, generating scenario-appropriate imagery

### Admin Interface

Access the admin interface at `http://localhost:8080/admin` to:

1. **View Current Scenario**: See which alternative internet scenario is currently active
2. **Switch Scenarios**: Choose from available scenarios (Etherweave, Retrofuturist, Cyberpunk, Solarpunk)
3. **Add Custom Scenarios**: Create your own alternative internet scenario by providing:
   - Scenario Name: A unique identifier for your scenario
   - Short Description: Brief explanation of the scenario
   - Full Scenario Description: Detailed guidelines for content generation

A "Browse Current Scenario" link takes you back to the main application with your selected scenario active.

## Project Structure

```
AlternativeInternet/
├── main.py               # Flask application entry point
├── chat.py               # Chat interface
├── image_generator.py    # Generates scenario-specific images
├── lm/                   # Language model clients
│   ├── base_lm_client.py       # Abstract base client interface
│   ├── openai_lm_client.py     # OpenAI implementation
│   └── cerebras_lm_client.py   # Cerebras implementation
├── prompts/              # Configuration for different scenarios
│   ├── retrofuturist.json
│   ├── etherweave.json
│   ├── cyberpunk.json
│   ├── solarpunk.json
│   └── scenario_manager.py
└── image_cache/          # Cached images for each scenario
```

## Extending the Project

### Adding a New Scenario

1. Create a new JSON configuration file in the `prompts/` directory
2. Add scenario-specific imagery to the `image_cache/` directory
3. Update the scenario manager to include your new scenario

## License

This project is licensed under the MIT License.