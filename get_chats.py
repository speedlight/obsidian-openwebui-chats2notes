import os
import requests
import json
import shutil

# Function to export chats from Open-WebUI to JSON
def export_chats():
    # Replace with your actual Open-WebUI API endpoint and Bearer token
    url = "http://localhost:3000/api/v1/chats/all"
    headers = {
        'Authorization': f'Bearer sk-ebe41e518bf54b13a7419adf23f938fc',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    
    # Print the status code and text of the response for debugging
    print(f"Status Code: {response.status_code}")
    # print(f"Chats data: {response.text}")

    if response.status_code == 200:
        try:
            chats_data = response.json()

            chats_file_path = os.path.join('.', f"exported_chats.json")
            with open(chats_file_path, 'w') as f:
                json.dump(chats_data, f, indent=4)
            print(f"Chats data exported successfully to {chats_file_path}!")
            
            # Create a directory to save individual chat files
            if os.path.exists('chats'):
                shutil.rmtree('chats')
            os.makedirs('chats')
            
            for chat_item in chats_data:
                chat_id = chat_item['id']
                chat_meta = chat_item['meta']
                chat_info = chat_item['chat']
                chat_title = chat_info['title']
                model_used = chat_info.get('models', [''])[0]
                created_at = chat_item['created_at']
                conversation = [
                        {
                            "role": msg['role'],
                            "content": msg['content']
                        }
                        for msg in chat_info.get('messages', [])
                ]
                tags = [ msg
                        for msg in chat_meta.get('tags', [])
                ]


                # Prepare the data to be saved
                chat_data = {
                    "id": chat_id,
                    "start_date": created_at,
                    "title": chat_title,
                    "model_used": model_used,
                    "conversation": conversation,
                    "tags": tags
                }

                # Save each chat to a separate JSON file
                chat_file_path = os.path.join('chats', f"{chat_id}.json")
                with open(chat_file_path, 'w') as f:
                    json.dump(chat_data, f, indent=4)
                print(f"Parsed chat {chat_id} exported successfully to {chat_file_path}!")

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
    else:
        print(f"Failed to export chats. Status code: {response.status_code}")

#Function to convert them to Markdown format
def transform_chats():
    chat_dir = 'chats'
    
    if not os.path.exists(chat_dir):
        print(f"The directory '{chat_dir}' does not exist.")
        return

    # Create a directory to save markdown files
    markdown_dir = os.path.join('chats', 'markdown')
    if os.path.exists(markdown_dir):
            shutil.rmtree(markdown_dir)
    os.makedirs(markdown_dir)
    
    for filename in os.listdir(chat_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(chat_dir, filename)
            
            with open(file_path, 'r') as f:
                chat_data = json.load(f)

                # Check if the 'title' key exists and print it
                if 'title' in chat_data:
                    title = chat_data['title']
                    print(f"Title: {title}")

                # Create the markdown content using a structured format
                markdown_content = (
                    f"---\n"
                    f"tags:\n"
                )
                for tag in chat_data['tags']:
                    markdown_content += f"  - {tag}\n"

                markdown_content += (
                    f"---\n"
                    f"**Title**: {chat_data['title']}\n"
                    f"## Chat\n"
                )
                
                for msg in chat_data['conversation']:
                    markdown_content += (
                        f">**Role**: {msg['role']}\n\n"
                        f"**Content**:\n"
                    )
                    markdown_content += f"{msg['content'].strip()}\n\n"

                # Append the closing delimiter
                markdown_content += (
                    f"**ID**: {chat_data['id']}\n"
                    f"**Model Used**: {chat_data['model_used']}\n\n"
                    f"---\n"
                )

                # Save the markdown content to a file
                markdown_file_path = os.path.join(markdown_dir, f"{chat_data['title']}.md")
                with open(markdown_file_path, 'w') as md_f:
                    md_f.write(markdown_content)
                print(f"Markdown file for chat {chat_data['id']} saved successfully.")

def copy_to_obsidian():
    # Define source and destination directories
    source_dir = 'chats/markdown/'
    destination_dir = '/path/to/Obsidian Vault/Open WebUI chats/'
    
    # Ensure the destination directory exists
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):  # Check if the file is a Markdown file
                src_file = os.path.join(root, file)
                print(src_file)
                dst_file = os.path.join(destination_dir, file)
                print(dst_file)
                
                # Copy the file to the destination directory
                shutil.copyfile(src_file, dst_file)
    
    print("Files copied successfully.")

if __name__ == "__main__":
    export_chats()
    transform_chats()
    copy_to_obsidian()
