from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
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
    output = new_paragraph
    context = {'output': output}
    return render(request, 'dashboard.html', context)


def replace_random_words(paragraph, replacement, num_words):
    words = re.findall(r'\w+', paragraph)
    random_words = random.sample(words, num_words)
    for word in random_words:
        paragraph = re.sub(r'\b{}\b'.format(word), replacement, paragraph)
    return paragraph

paragraph = "For God So Loved The world, he gave his only son, so that whoever beleives in him should not parish, but have eternal life."
replacement_word = "___"
num_words_to_replace=3
new_paragraph = replace_random_words(paragraph, replacement_word, num_words_to_replace)
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


