import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
import json
import requests
from django.template.defaultfilters import slugify
import os
from django.utils import timezone

import datetime
from .models import RoadProgress
from .models import Settings
from .models import CustomRoads
from django.views.decorators.http import require_POST
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
import io
from datetime import timedelta
from django.utils.timezone import is_aware, make_aware
from PIL import Image, ImageDraw
import math
from django.http import FileResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from xhtml2pdf import pisa
from road_bible.models import Favorites
from road_bible.models import Friends
from django.contrib.auth.models import User


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "favicon.png").open("rb")
    return FileResponse(file)


def my_view(request):
    # Update this to the directory containing JSON files
    json_directory = 'static/roads'

    # Get a list of all JSON files in the directory
    json_files = [file for file in os.listdir(
        json_directory) if file.endswith('.json')]

    combined_data = []

    for json_file in json_files:
        with open(os.path.join(json_directory, json_file), 'r') as file:
            data = json.load(file)
            number_of_groups = len(data)
            combined_data.append(
                {'parsed_data': data, 'num_groups': number_of_groups})

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
        current_sentence_index = int(
            request.POST.get("current_sentence_index", 0))
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


@csrf_exempt
def approve(request):
    data = json.loads(request.body)
    title = data['title']
    user = data['username']
    send_mail(
        f"{title} Road approval",
        f"{user} wants you to approve their {title} Road",
        "support@roadsbible.com",
        ["jadongearhart@icloud.com"],
    )
    return HttpResponse("Success", status="200")


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
        # Replace this with the actual sentence index retrieved from the database.
        sentence_index = 0
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


@csrf_exempt
def save_verses(request):
    try:
        data = json.loads(request.body)
        verses = data.get('verses', [])
        title = data.get('title', '')
        creator = data.get('username', '')

        custom_road, created = CustomRoads.objects.get_or_create(
            title=title,
            creator=creator,
            defaults={'verses': verses}
        )

        if not created:
            custom_road.verses = verses
            custom_road.save()

        return JsonResponse({'status': 'Data saved successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@csrf_exempt
def user_dash(request):
    data = json.loads(request.body)
    user = data.get('username', '')

    if user:
        roads = CustomRoads.objects.filter(creator=user)
        combined_data = []

        for road in roads:
            title = road.title
            verses = road.verses
            num = 0  # Initialize num for each road
            descriptions = []
            urls = []
            for verse in verses:
                num += 1  # Increment num for each verse
                description = verse.get('description')
                url = verse.get('url')
                if description:
                    descriptions.append(description)
                    urls.append(url)

            road_data = {
                'title': title,
                'num': num,
                'url': urls,

                'creator': user,
                'descriptions': descriptions
            }
            combined_data.append(road_data)

        response_data = {
            'combined_data': combined_data
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Missing or invalid username'})


@csrf_exempt
def verses_view(request, group_name):
    data = json.loads(request.body)
    print(data)
    title = data['title']
    user = data['username']
    custom = data['custom']
    print('whyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
    if custom == 'yes':
        # Fetch data from the database
        print('custom')
        print(title)
        creator = user
        try:
            custom_road = CustomRoads.objects.get(title=title, creator=user)
            verses = custom_road.verses
        except CustomRoads.DoesNotExist:
            return JsonResponse({'error': 'Custom road not found'}, status=404)
    else:

        atitle = group_name.replace("%20", "_")
        # Fetch data from the JSON file
        json_file_path = f'static/roads/{atitle}.json'
        with open(json_file_path, 'r') as json_file:
            verses_info = json.load(json_file)
            verses = verses_info

        print("Parsed JSON:", verses)

    # Initialize an empty list to store retrieved verses
    retrieved_verses = []
    translation = Settings.objects.get(user_name=user)
    translation_value = translation.translation
    print(translation_value)

    # API integration: Loop through each verse info and retrieve the text
    api_base_url = f'https://jsonbible.com/search/verses.php?json={{verse_id}}'
    for verse_info in verses:
        print(verse_info['chapter'])
        send = {"book": verse_info['book_name'],  "chapter": str(verse_info['chapter']),
                "verse": str(verse_info['verse_number']), "found": 1,  "version": translation_value.lower()}
        api_url = api_base_url.format(verse_id=json.dumps(send))
        print(api_url)
        api_response = requests.get(api_url)
        print("API Response:", api_response.text)

        api_data = api_response.json()
        print("API Data:", api_data)

        verse_text = api_data.get('verse', 'Verse not found')
        print("Verse Text:", verse_text)

        reference = f"{api_data['book']} {api_data['chapter']}:{api_data['verses']} ({translation_value})"
        retrieved_verses.append({
            'verse': api_data.get('text', 'Verse not found'),
            'reference': reference,
        })  # Append the API data to the list
    try:
        s = group_name.replace("%20", " ")

        print("AAA")
        print(f"GR: {s}")

        favorites = Favorites.objects.filter(
            user_name=user, title="/roads/" + s).values()
        faavs = []
        for favs in favorites:
            faavs.append(favs["index"])
            print(favs["index"])
        print(favorites)
        print(faavs)
    except Favorites.DoesNotExist:
        print("none")
        faavs = []
    s = group_name.replace("%20", " ")
    preogressIndex = 0
    progress = RoadProgress.objects.filter(user_name=user, road=s)
    if progress.exists():
        preogressIndex = progress.get().index

    else:
        print("Progress not found or index not available")

    # Prepare the JSON response
    response_data = {
        'progress': preogressIndex,
        'favorites': faavs,
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

            complete = data.get('complete', False)
            user_name = data.get('username', "unknown")
            cus = data.get('isCustom', False)
            da = timezone.now()
            # Check if a RoadProgress entry with the same road and user_name exists
            existing_progress = RoadProgress.objects.filter(
                road=road, user_name=user_name).first()

            if existing_progress:
                # If an entry already exists, update the index
                existing_progress.index = index
                existing_progress.complete = complete
                existing_progress.isCustom = cus
                existing_progress.date = da
                existing_progress.save()
            else:
                # If no entry exists, create a new one
                RoadProgress.objects.create(
                    user_name=user_name, road=road, index=index, complete=complete, date=da, isCustom=cus)

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
            progress = RoadProgress.objects.filter(
                user_name=user_name, road=road_name).first()
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
def get_last_road(request):
    ah = json.loads(request.body)
    user = ah.get('username')
    basestuff = RoadProgress.objects.filter(user_name=user)
    stuff = basestuff.order_by('-date').first()

    print(stuff)
    if stuff is not None:
        serialized_stuff = serializers.serialize('json', [stuff, ])
        return JsonResponse(serialized_stuff, status=200, safe=False)
    else:
        return JsonResponse({"error": "No data found"}, status=404)


@csrf_exempt
def gameify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data =>>', data)

            user = data.get('username', 'unknown')
            dbdata = RoadProgress.objects.filter(user_name=user)
            stuff = dbdata.order_by('-date').first()
            # Check if date exists for the user and add seven days to it

            # Initialize a variable to store the total sum
            total_sum = 0
            for da in dbdata:
                # Consider using a different attribute or check if 'index' exists in your model
                if hasattr(da, 'index') and da.index > 0:
                    numverse = da.index + 1
                    total_sum += numverse  # Add the current value to the total sum
                else:
                    print('Not started or attribute issue')

            # After the loop, return the total sum or a message if it's not started
            if total_sum > 0:
                return JsonResponse({'numverses': total_sum, 'lastdate': stuff.date, 'lastroad': stuff.road, 'islastroadcustom': stuff.isCustom}, status=200)
            else:
                return JsonResponse({'numverses': 'Not started'}, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    else:
        return JsonResponse({'error': 'This is a POST only endpoint, sorry.'}, status=405)


@require_POST
@csrf_exempt
def newfriend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('name')
        friend_to_add = data.get('friendtoadd')
        imp = data.get('username')

        try:
            # Checking if the user exists
            user_instance = User.objects.get(username=imp)

            if not friend_to_add or not Friends.objects.filter(username=friend_to_add).exists():

                # If friend's name is absent or doesn't exist, save with an empty friend array
                user_friends, _ = Friends.objects.get_or_create(
                    username=username, userid=imp, defaults={'friends': []})
                return JsonResponse({'message': 'Data saved with an empty friend array!'})

            # Friend to add exists, proceed to add
            user_friends, _ = Friends.objects.get_or_create(
                username=username, userid=imp, defaults={'friends': []})
            friends_list = user_friends.friends

            if friend_to_add not in friends_list:
                friends_list.append(friend_to_add)
                user_friends.friends = friends_list
                user_friends.save()
                return JsonResponse({'message': f'{friend_to_add} added to friends!'})
            else:
                return JsonResponse({'message': f'{friend_to_add} is already a friend!'})

        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found!'})

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
@require_POST
def getfrienddata(request):
    d = json.loads(request.body)
    importantuser = d.get('username')
    fdb = Friends.objects.filter(userid=importantuser)
    friends = []
    friendspracticedates = []
    friendspracticetitles = []
    obj = {

    }
    namee = fdb.first().username
    final = []
    for rawname in fdb:
        for name in rawname.friends:

            basestuff = RoadProgress.objects.filter(user_name=importantuser)
            stuff = basestuff.order_by('-date').first()
            print(stuff.road)
            print(stuff.date)
            friends.append(name)

            friendspracticedates.append(stuff.date)
            try:
                friendsroads = CustomRoads.objects.filter(
                    creator=importantuser)
                for r in friendsroads:

                    print(r.title)
                    obj = {
                        "title": r.title,
                        "maker": name
                    }
                    final.append(obj)

                friendspracticetitles.append(stuff.road)

            except CustomRoads.DoesNotExist:
                print('this user has no roads')
    return JsonResponse({'friendsnames': friends, "friendspracticedates": friendspracticedates, "friendspracticetitles": friendspracticetitles, "friendsroads": final, "name": namee}, status=200)


@csrf_exempt
def settings(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data =>>', data)

            user = data.get('username', "unknown")
            userget, created = Settings.objects.get_or_create(user_name=user)

        # Loop through the data and update the corresponding values
            for key, value in data.items():
                if key != 'username':
                    setattr(userget, key, value)

            userget.save()

            if created:
                print('yay')
            # The user was just created
            # You can do something specific here if needed

            dataa = serializers.serialize('json', [userget])
            return HttpResponse(dataa, content_type='application/json', status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'This is a POST only endpoint, sorry.'}, status=405)


@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request):
    print('tes')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = data.get('username')
            road = data.get('road')
            try:
                # Assuming you have a model named 'CustomRoads' that represents your database table
                # Use filter to get the queryset
                items_to_delete = CustomRoads.objects.filter(
                    creator=user, title=road)
                # Loop through the queryset and print the items for debugging
                for item in items_to_delete:
                    print(f"Deleting item:")
                    print(f"Title: {item.title}")
                    item.delete()

                return JsonResponse({'message': 'Rows deleted successfully'})
            except CustomRoads.DoesNotExist:
                return JsonResponse({'error': 'Rows not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def getroads(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('username')
        usertoget = data.get('usertoget')
        road = data.get('road')
        try:
            response = list(CustomRoads.objects.filter(
                title=road, creator=usertoget))

            # Serialize the response to JSON
            response_data = serializers.serialize('json', response)

            # Deserialize the JSON string back to a Python object
            response_data = json.loads(response_data)

            return JsonResponse({'data': response_data}, status=200)

        except CustomRoads.DoesNotExist:
            return HttpResponse('Whoops! That road does not exist', status=404)
    else:
        return HttpResponse('POST only, man!', status=400)


@csrf_exempt
def pdf(request):

    username = request.GET.get('username')
    title = request.GET.get('title')
    custom = request.GET.get('custom')

    dataa = {
        'title': title,
        'custom': custom,
        'username': username,
    }

    response = requests.post(
        f'https://www.roadsbible.com/roads/{title}/', json=dataa)
    response.raise_for_status()  # Check for HTTP request errors
    res = response.json()
    print('res', res)
    fin = {
        "res": res,
        "title": title,
    }
    template = get_template('flashcards.html')
    html_content = template.render({'fin': fin})

    # Create a Django HttpResponse with PDF content

    # Create a Django HttpResponse with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'

    # Create a PDF using xhtml2pdf
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)

    if not pdf.err:
        response.write(result.getvalue())
        result.close()
        return response

    # Create a file-like buffer to receive PDF data.


@csrf_exempt
def newfavorites(request):
    data = json.loads(request.body)
    user = data.get('username')
    road = data.get('road')
    title = data.get('title')
    index = data.get('index')
    verse = data.get('verse')
    Favorites.objects.get_or_create(
        user_name=user, title=title, index=index, verse=verse, road=road)
    return HttpResponse("Done!", status=200)


@csrf_exempt
def getfavorites(request):
    data = json.loads(request.body)
    user = data.get('username')
    try:
        s = list(Favorites.objects.filter(user_name=user).values())
    except Favorites.DoesNotExist:
        return HttpResponse("No favorites for this user", status=404)
    return JsonResponse(s, safe=False, status=200)
