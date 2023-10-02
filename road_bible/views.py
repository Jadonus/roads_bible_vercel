from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
import json
import requests
from django.template.defaultfilters import slugify
import os
from django.views.decorators.csrf import csrf_exempt
from .models import RoadProgress
from django.core import serializers

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "favicon.png").open("rb")
    return FileResponse(file)
from .forms import ReplaceWordsForm
import re
def my_view(request):
    json_directory = 'static/roads'  # Update this to the directory containing JSON files

    # Get a list of all JSON files in the directory
    json_files = [file for file in os.listdir(json_directory) if file.endswith('.json')]

    combined_data = []

    for json_file in json_files:
        with open(os.path.join(json_directory, json_file), 'r') as file:
            data = json.load(file)
            number_of_groups = len(data)
            combined_data.append({'parsed_data': data, 'num_groups': number_of_groups})

    context = {
        'combined_data': combined_data,
    }

    return JsonResponse(context)







@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "favicon.png").open("rb")
    return FileResponse(file)

def save_user_progress(request):
    if request.method == "POST" and request.user.is_authenticated:
        current_sentence_index = int(request.POST.get("current_sentence_index", 0))
        hidden_word_indices = request.POST.get("hidden_word_indices", "")
        # Save the progress in the database (using UserProgress model)
        # ...

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

def get_user_progress(request):
    if request.user.is_authenticated:
        # Retrieve the progress from the database (using UserProgress model)
        # ...

        return JsonResponse({
            "current_sentence_index": current_sentence_index,
            "hidden_word_indices": hidden_word_indices,
        })

    return JsonResponse({}, status=401)
def custom_404(request, exception):
    return render(request, '404.html', status=404)
def saveold_progress(request):
    if request.method == 'POST' and request.user.is_authenticated:
        username = request.user.username
        sentence_index = int(request.POST.get('sentence_index', 0))
        # Save the user's progress in the database or any other data store
        # For example, you could use Django models to save the progress in the database.
        # Your implementation may vary based on your project's structure.
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



def restore_progress(request):
    if request.method == 'GET' and request.user.is_authenticated:
        # Retrieve the user's progress from the database or data store
        # For example, you could use Django models to fetch the progress from the database.
        # Your implementation may vary based on your project's structure.
        sentence_index = 0  # Replace this with the actual sentence index retrieved from the database.
        return JsonResponse({'sentence_index': sentence_index})
    return JsonResponse({'sentence_index': 0})

def adjust_verse_number(book_id, chapter, verse_number):
    book_id = int(book_id)
    chapter = int(chapter)
    verse_number = int(verse_number)
    print(book_id)
    print(chapter)
    print(verse_number)
    adjusted_number = str(book_id * 1000000 + chapter * 1000 + verse_number)
    ads = str(adjusted_number)
    return ads 
    print(ads)


from django.http import JsonResponse

def verses_view(request, group_name):
    json_file_path = f'static/roads/{group_name}.json'
    with open(json_file_path, 'r') as json_file:
        verses_info = json.load(json_file)
        print("Parsed JSON:", verses_info)

    # Initialize an empty list to store retrieved verses
    retrieved_verses = []

    # API integration: Loop through each verse info and retrieve the text
    api_base_url = 'https://bible-go-api.rkeplin.com/v1/books/1/chapters/1/{verse_id}?translation=NIV'
    for verse_info in verses_info:
        verse_id = adjust_verse_number(
            verse_info['book_id'],
            verse_info['chapter'],
            verse_info['verse_number']
        )
        api_url = api_base_url.format(verse_id=verse_id)
        print(api_url)
        api_response = requests.get(api_url)
        print("API Response:", api_response.text)

        api_data = api_response.json()
        print("API Data:", api_data)

        verse_text = api_data.get('verse', 'Verse not found')
        print("Verse Text:", verse_text)
        versedata1 = api_data.get('book', {}).get('name', 'Book not found')
        versedata2 = api_data.get('chapterId')
        versedata3 = api_data.get('verseId')
        reference = f"{api_data['book']['name']} {api_data['chapterId']}:{api_data['verseId']} (NIV)"
        retrieved_verses.append({
            'verse': api_data.get('verse', 'Verse not found'),
            'reference': reference,
        })  # Append the API data to the list

    # Prepare the JSON response
    response_data = {
        'group_name': group_name,
        'verses': retrieved_verses,
    }

    # Return the data as JSON
    return JsonResponse(response_data)

#
#
#
#
def verses_eli_view(request, group_name):
    retrieved_verses = [
        {
            'verse': 'See to it that no one takes you captive through hollow and desceptive philosophy, which deoends on human tradition and the elemental spiritual forces of this world rather than on Christ. Collossians 2:8'
        }
    ]
    
    context = {
        'group_name': group_name,
        'verses': retrieved_verses,
    }

    return render(request, 'defaultroadload.html', context)
@csrf_exempt
def save_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data =>', data)
            road = data.get('road', 'default')
            index = data.get('index', 0)

            complete=data.get('complete', False)
            user_name = data.get('username', "unknown")

            # Check if a RoadProgress entry with the same road and user_name exists
            existing_progress = RoadProgress.objects.filter(road=road, user_name=user_name).first()

            if existing_progress:
                # If an entry already exists, update the index
                existing_progress.index = index
                existing_progress.complete= complete
                existing_progress.save()
            else:
                # If no entry exists, create a new one
                RoadProgress.objects.create(user_name=user_name, road=road, index=index, complete=complete)

            return JsonResponse({'message': 'Progress saved successfully'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests'}, status=405)


@csrf_exempt
def get_saved_progress(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.body)
            print('info =>', info)
            user_name = info.get('username', "unknown")
            road_name = info.get('road', 'default')
            progress = RoadProgress.objects.filter(user_name=user_name, road=road_name).first()
            # Check if progress exists before attempting to serialize it
            if progress:
                progress_data = {
                    'user_name': progress.user_name,
                    'road': progress.road,
                    'index': progress.index,
                }
                return JsonResponse({'progress': progress_data}, status=200)
            else:
                return JsonResponse({'error': 'Progress not found'}, status=404)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'This endpoint only accepts POST requests'}, status=405)


@csrf_exempt
def gameify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data =>>', data)

            user = data.get('username', "unknown")
            dbdata = RoadProgress.objects.filter(user_name=user)

            # Initialize a variable to store the total sum
            total_sum = 0

            for da in dbdata:
                if da.index > 0:
                    numverse = da.index + 1
                    total_sum += numverse  # Add the current value to the total sum
                else:
                    print('not started')

            # After the loop, return the total sum
            if total_sum > 0:
                return JsonResponse({'numverses': total_sum}, status=200)
            else:
                return JsonResponse({'numverses': 'Not started'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'This is a POST only endpoint, sorry.'}, status="405")
   
    


