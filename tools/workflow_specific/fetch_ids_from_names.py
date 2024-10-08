import argparse
import os
import openai
import json

# Initialize OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up argument parser
parser = argparse.ArgumentParser(description='Fetch assistant and vector store IDs by repo and branch names.')
parser.add_argument('--repository', required=True, help='The name of the repository')
parser.add_argument('--branch', required=True, help='The name of the branch')
parser.add_argument('--output', required=True, help='The name of the output JSON file')
args = parser.parse_args()

repo_name = args.repository
branch_name = args.branch
output_file = args.output

tag_to_find = f"{repo_name}-{branch_name}"

# Function to fetch assistant_id using the assistant name

def get_assistant_id_by_name():
    """
    Fetches the assistant ID based on the assistant name pattern.
    """
    assistants = openai.beta.assistants.list()
    for assistant in assistants:
        if tag_to_find in assistant.name:
            print(assistant.name)
            print(assistant.id)
            return assistant.id
    print(f"Assistant not found for {tag_to_find}")
    return None

# Function to fetch vector_store_id using the vector store name

def get_vector_store_id_by_name():
    """
    Fetches the vector store ID based on the naming convention.
    """
    vector_stores = openai.beta.vector_stores.list()
    for vector_store in vector_stores:
        if tag_to_find in vector_store.name:
            print(vector_store.name)
            print(vector_store.id)
            return vector_store.id
    print(f"Vector store not found for {tag_to_find}")
    return None

assistant_id = get_assistant_id_by_name()
vector_store_id = get_vector_store_id_by_name()

# Write IDs to a JSON output file
output_data = {}
if assistant_id:
    output_data['repo_assistant_id'] = assistant_id
if vector_store_id:
    output_data['repo_vector_store_id'] = vector_store_id

with open(output_file, 'w') as file:
    json.dump(output_data, file, indent=4)
print(f"Output written to {output_file}")
