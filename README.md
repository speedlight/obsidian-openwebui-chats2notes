# Open-WebUI Chat Exporter Script

## Overview

This Python script is designed to automate the process of exporting all chat data from an Open-WebUI, transforming simpler JSON and Markdown formats, and then copying it to an Obsidian Vault directory.
The script uses the `requests` library to interact with the Open-WebUI API, the `json` library for parsing JSON data, and the `shutil` library for file operations.

## Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **Requests Library**: Install using pip if not already available:
   ```bash
   pip install requests
   ```
3. **Open-WebUI API Access**: Ensure you have the correct URL and Bearer token to access the Open-WebUI API.
> The script assumes that the Open-WebUI API is running locally at `http://localhost:3000`.

## Installation

1. Clone or download this repository.
2. Place the script in your preferred directory.

## Usage

### Exporting Chats

The script starts by exporting all chat data from the specified Open-WebUI instance to a JSON file named `exported_chats.json` in the current directory.

#### Configuration
Edit the script and replace the placeholders in the `headers` dictionary:
```python
url = "http://localhost:3000/api/v1/chats/all"
headers = {
    'Authorization': f'Bearer YOUR_BEARER_TOKEN',
    'Content-Type': 'application/json'
}
```
One can inspect the json file to see the complete chat object in case aditional information is wanted to be added into the note markdown file.

Run the script using Python:
```bash
python chat_exporter.py
```

### Transforming Chats to Markdown

After exporting, the script transforms each chat into a separate Markdown file located in the `chats/markdown` directory.
Each Markdown file corresponds to one chat and includes the conversation history, title, tags, and model used.

### Copying to Obsidian Vault

The script then copies all Markdown files from the `chats/markdown` directory to a specified Obsidian Vault directory in a notes folder called `Open WebUI chats`.
Ensure that the destination directory exists or modify the path as needed.

