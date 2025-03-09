from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    current_year = datetime.now().year

    context = {
        'year': current_year,
    }

    return render(
        request = request,
        template_name = 'core/home.html',
        context = context,
    )
