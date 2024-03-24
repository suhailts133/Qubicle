# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from scripts.new import combined_function
from .forms import ImageForm
from django.conf import settings
import json
import os  
from .models import JSONFile
from django.shortcuts import redirect
from .utils import delete_uploaded_images, delete_json_files
import random
BASE_DIR = settings.BASE_DIR

def home(request):
    form = ImageForm()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()

            # Display a success message with only the image name
            image_name = image_instance.image.name.split('/')[-1]  # Extracts only the image name
            messages.success(request, f'Image "{image_name}" uploaded successfully.')

            # Check if the 'Process Images' button is pressed
            if 'action' in request.POST and request.POST['action'] == 'process_images':
                try:
                    # Call the combined_function with the images folder path
                    json_file_path = combined_function('media/uploaded_images/')
                    messages.success(request, f'Repeated questions saved in: {json_file_path}')
                except Exception as e:
                    messages.error(request, f'Error processing images: {str(e)}')

                return redirect('home')

    return render(request, 'home.html', {'form': form})


def process_images(request):
    try:
        # Call the combined_function with the images folder path
        json_file_path = combined_function('media/uploaded_images/')
        return JsonResponse({'success': True, 'message': f'Repeated questions saved in: {json_file_path}'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def view_cleaned_json(request):
    # Updated path to the cleaned.json file using the BASE_DIR
    combined_json_path = os.path.join(BASE_DIR, 'json', 'final_output.json')

    try:
        with open(combined_json_path, 'r') as json_file:
            final_data = json.load(json_file)
    except FileNotFoundError:
        final_data = None

    return render(request, 'result.html', {'final_data': final_data})


def model_qp(request):
    combined_json_path = os.path.join(BASE_DIR, 'json', 'repeated.json')

    try:
        with open(combined_json_path, 'r') as json_file:
            questions_data = json.load(json_file)

            # Combine all questions into a single list
            all_questions = [question for questions in questions_data.values() for question in questions]

            if request.method == 'GET':
                # Shuffle the list of questions initially
                random.shuffle(all_questions)

                # Select unique questions
                unique_questions = []
                seen = set()
                for question in all_questions:
                    if question['sentence'] not in seen:
                        unique_questions.append(question)
                        seen.add(question['sentence'])

                # Select the first 15 unique questions (or less if there are fewer than 15)
                random_questions = unique_questions[:min(15, len(unique_questions))]

            elif request.method == 'POST' and 'change-questions' in request.POST:
                # Shuffle the list of questions when changing questions
                random.shuffle(all_questions)
                # Select the first 15 questions (or less if there are fewer than 15)
                random_questions = all_questions[:min(15, len(all_questions))]

    except FileNotFoundError:
        random_questions = None

    return render(request, 'model_qp.html', {'random_questions': random_questions})


def json_files(request):
    # Retrieve all JSON files from the database
    json_files = JSONFile.objects.all()
    return render(request, 'inventory.html', {'json_files': json_files})



def display_json_content(request, filename):
    # Append .json extension to the filename
    filename_with_extension = f"{filename}.json"

    json_folder = os.path.join(settings.MEDIA_ROOT, 'uploaded_json')  # Assuming JSON files are uploaded to this folder
    json_file_path = os.path.join(json_folder, filename_with_extension)

    try:
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            
    except FileNotFoundError:
        json_data = None

    return render(request, 'stored_important.html', {'json_data': json_data})


def model_qp_stored(request, filename):
    filename_with_extension = f"{filename}Model.json"
    json_folder = os.path.join(settings.MEDIA_ROOT, 'uploaded_QP')
    model_qp_path = os.path.join(json_folder, filename_with_extension)
    

    try:
        with open(model_qp_path, 'r') as json_file:
            questions_data = json.load(json_file)

            # Combine all questions into a single list
            all_questions = [question for questions in questions_data.values() for question in questions]

            if request.method == 'GET':
                unique_questions = set()  # Set to store unique questions
                while len(unique_questions) < 15:
                    # Shuffle the list of questions initially
                    random.shuffle(all_questions)
                    # Select unique questions until we have 15
                    unique_questions = set(all_questions[:min(15, len(all_questions))])
            
            elif request.method == 'POST' and 'change-questions' in request.POST:
                # Shuffle the list of questions when changing questions
                random.shuffle(all_questions)
                # Select the first 15 questions (or less if there are fewer than 15)
                unique_questions = all_questions[:min(15, len(all_questions))]

    except FileNotFoundError:
        unique_questions = None

    return render(request, 'stored_modelqp.html', {'random_questions': list(unique_questions)})


def delete_all_data(request):
    if request.method == 'POST':
        delete_uploaded_images()
        delete_json_files()
        return redirect('home') 
    return redirect('home')  
