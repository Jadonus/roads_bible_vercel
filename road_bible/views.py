from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
import json
import requests
from django.template.defaultfilters import slugify
import os

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
@login_required
def my_view(request):
    json_directory = 'static/roads'  # Update this to the directory containing JSON files

    # Get a list of all JSON files in the directory
    json_files = [file for file in os.listdir(json_directory) if file.endswith('.json')]

    # Initialize a list to store parsed data for all files
    parsed_data = []

    for json_file in json_files:
        with open(os.path.join(json_directory, json_file), 'r') as file:
            data = json.load(file)
            parsed_data.extend(data)  # Extend the list with data from the current file

    context = {
        'parsed_data': parsed_data,
    }

    return render(request, 'dashboard.html', context)









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
def save_progress(request):
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

def verses_view(request, group_name):
    json_file_path = f'static/roads/{group_name}.json'
    with open(json_file_path, 'r') as json_file:
        verses_info = json.load(json_file)
        print("Parsed JSON:", verses_info)

    title = 'Title not found'
    img = 'No image found'

    # Loop through each verse info and retrieve the title
    for verse_info in verses_info:
        title = verse_info.get('title')

        imgname = verse_info.get('img')
        if title and img:
            break
    # Initialize an empty list to store retrieved verses
    retrieved_verses = []
    '''  gradient = os.path.join(settings.STATIC_ROOT, 'gradient.jpg')
    # Logic to make a gradient title image.
    img = Image.open(gradient)

    msg = title
    font = ImageFont.truetype('static/libsans.otf', 170)

# Get text dimensions using ImageFont.getsize
    text_width, text_height = font.getsize(msg)

# Get image dimensions
    image_width, image_height = img.size

# Create a drawing object
    draw = ImageDraw.Draw(img)

# Calculate the starting point for the centered text
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

# Draw the text at the centered position
    draw.text((x, y), msg, font=font, fill=(255, 255, 255))
    image_path = os.path.join(settings.STATIC_ROOT, imgname)

   img.save(image_path) 
   '''
    #
    ##
    #
    # . API grabbing and such...
    #
    #

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

        retrieved_verses.append(verse_text)

    context = {
        'group_name': group_name,
        'verses': retrieved_verses,
    }

    return render(request, 'defaultroadload.html', context)