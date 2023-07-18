from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


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
