from django.shortcuts import render
from django.contrib.auth.models import User

from db.base.models import Transponder, Satellite


def home(request):
    """View to render index page."""
    satellites = Satellite.objects.all()
    transponders = Transponder.objects.all()
    contributors = User.objects.filter(is_active=1)

    return render(request, 'base/home.html', {'satellites': satellites,
                                              'transponders': transponders,
                                              'contributors': contributors})
