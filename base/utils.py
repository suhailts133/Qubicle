# utils.py
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR

def delete_uploaded_images():
    folder_path = 'media/uploaded_images/'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {file_path}, {e}")

def delete_json_files():
    json_files = os.path.join(BASE_DIR, 'json')
    folder_path = json_files
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {file_path}, {e}")