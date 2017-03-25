import ephem
import logging
import requests
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.db.models import Count

from db.base.models import Mode, Transmitter, Satellite, Suggestion, DemodData
from db.base.forms import SuggestionForm
from db.base.helpers import get_apikey


logger = logging.getLogger('db')


@cache_page(settings.CACHE_TTL)
def home(request):
    """View to render home page."""
    satellites = Satellite.objects.all()
    transmitters = Transmitter.objects.all().count()
    suggestions = Suggestion.objects.all().count()
    contributors = User.objects.filter(is_active=1).count()
    return render(request, 'base/home.html', {'satellites': satellites,
                                              'transmitters': transmitters,
                                              'contributors': contributors,
                                              'suggestions': suggestions})


def custom_404(request):
    """Custom 404 error handler."""
    return HttpResponseNotFound(render(request, '404.html'))


def custom_500(request):
    """Custom 500 error handler."""
    return HttpResponseServerError(render(request, '500.html'))


def robots(request):
    data = render(request, 'robots.txt', {'environment': settings.ENVIRONMENT})
    response = HttpResponse(data,
                            content_type='text/plain; charset=utf-8')
    return response


def satellite_position(request, sat_id):
    sat = get_object_or_404(Satellite, norad_cat_id=sat_id)
    try:
        satellite = ephem.readtle(
            str(sat.name),
            str(sat.tle1),
            str(sat.tle2)
        )
    except:
        data = {}
    else:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        satellite.compute(now)
        data = {
            'lon': '{0}'.format(satellite.sublong),
            'lat': '{0}'.format(satellite.sublat)
        }
    return JsonResponse(data, safe=False)


def satellite(request, norad):
    """View to render home page."""
    satellite = get_object_or_404(Satellite, norad_cat_id=norad)
    suggestions = Suggestion.objects.filter(satellite=satellite)
    modes = Mode.objects.all()

    url = '{0}{1}'.format(settings.SATELLITE_POSITION_ENDPOINT, norad)

    try:
        sat_position = requests.get(url).json()
    except:
        sat_position = ''

    return render(request, 'base/satellite.html', {'satellite': satellite,
                                                   'suggestions': suggestions, 'modes': modes,
                                                   'sat_position': sat_position,
                                                   'mapbox_id': settings.MAPBOX_MAP_ID,
                                                   'mapbox_token': settings.MAPBOX_TOKEN})


@login_required
@require_POST
def suggestion(request):
    """View to process suggestion form"""
    suggestion_form = SuggestionForm(request.POST)
    if suggestion_form.is_valid():
        suggestion = suggestion_form.save(commit=False)
        suggestion.user = request.user
        suggestion.save()

        # Notify admins
        admins = User.objects.filter(is_superuser=True)
        site = get_current_site(request)
        subject = '[{0}] A new suggestion was submitted'.format(site.name)
        template = 'emails/new_suggestion.txt'
        saturl = '{0}{1}'.format(
            site.domain,
            reverse('satellite', kwargs={'norad': suggestion.satellite.norad_cat_id})
        )
        data = {
            'satname': suggestion.satellite.name,
            'saturl': saturl,
            'site_name': site.name
        }
        message = render_to_string(template, {'data': data})
        for user in admins:
            try:
                user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
            except:
                logger.error(
                    'Could not send email to user',
                    exc_info=True
                )

        messages.success(request, ('Your suggestion was stored successfully. '
                                   'Thanks for contibuting!'))
        return redirect(reverse('satellite', kwargs={'norad': suggestion.satellite.norad_cat_id}))
    else:
        logger.error(
            'Suggestion form was not valid {0}'.format(suggestion_form.errors),
            exc_info=True,
            extra={
                'form': suggestion_form.errors,
            }
        )
        messages.error(request, 'We are sorry, but some error occured :(')
        return redirect(reverse('home'))


def about(request):
    """View to render about page."""
    return render(request, 'base/about.html')


def faq(request):
    """View to render faq page."""
    return render(request, 'base/faq.html')


def stats(request):
    """View to render stats page."""
    satellites = Satellite.objects \
                          .values('name', 'norad_cat_id') \
                          .annotate(count=Count('telemetry_data')) \
                          .order_by('-count')
    observers = DemodData.objects \
                         .values('observer') \
                         .annotate(count=Count('observer')) \
                         .order_by('-count')
    return render(request, 'base/stats.html', {'satellites': satellites,
                                               'observers': observers})


@cache_page(settings.CACHE_TTL)
def statistics(request):
    """View to create statistics endpoint."""
    satellites = Satellite.objects.all()
    transmitters = Transmitter.objects.all()
    modes = Mode.objects.all()

    total_satellites = satellites.count()
    total_transmitters = transmitters.count()
    alive_transmitters = transmitters.filter(alive=True).count()
    alive_transmitters_percentage = '{0}%'.format(round((float(alive_transmitters) /
                                                         float(total_transmitters)) * 100, 2))

    mode_label = []
    mode_data = []
    for mode in modes:
        tr = transmitters.filter(mode=mode).count()
        mode_label.append(mode.name)
        mode_data.append(tr)

    band_label = []
    band_data = []

    # <30.000.000 - HF
    filtered = transmitters.filter(downlink_low__lt=30000000).count()
    band_label.append('HF')
    band_data.append(filtered)

    # 30.000.000 ~ 300.000.000 - VHF
    filtered = transmitters.filter(downlink_low__gte=30000000,
                                   downlink_low__lt=300000000).count()
    band_label.append('VHF')
    band_data.append(filtered)

    # 300.000.000 ~ 1.000.000.000 - UHF
    filtered = transmitters.filter(downlink_low__gte=300000000,
                                   downlink_low__lt=1000000000).count()
    band_label.append('UHF')
    band_data.append(filtered)

    # 1G ~ 2G - L
    filtered = transmitters.filter(downlink_low__gte=1000000000,
                                   downlink_low__lt=2000000000).count()
    band_label.append('L')
    band_data.append(filtered)

    # 2G ~ 4G - S
    filtered = transmitters.filter(downlink_low__gte=2000000000,
                                   downlink_low__lt=4000000000).count()
    band_label.append('S')
    band_data.append(filtered)

    # 4G ~ 8G - C
    filtered = transmitters.filter(downlink_low__gte=4000000000,
                                   downlink_low__lt=8000000000).count()
    band_label.append('C')
    band_data.append(filtered)

    # 8G ~ 12G - X
    filtered = transmitters.filter(downlink_low__gte=8000000000,
                                   downlink_low__lt=12000000000).count()
    band_label.append('X')
    band_data.append(filtered)

    # 12G ~ 18G - Ku
    filtered = transmitters.filter(downlink_low__gte=12000000000,
                                   downlink_low__lt=18000000000).count()
    band_label.append('Ku')
    band_data.append(filtered)

    # 18G ~ 27G - K
    filtered = transmitters.filter(downlink_low__gte=18000000000,
                                   downlink_low__lt=27000000000).count()
    band_label.append('K')
    band_data.append(filtered)

    # 27G ~ 40G - Ka
    filtered = transmitters.filter(downlink_low__gte=27000000000,
                                   downlink_low__lt=40000000000).count()
    band_label.append('Ka')
    band_data.append(filtered)

    mode_data_sorted, mode_label_sorted = zip(*sorted(zip(mode_data, mode_label), reverse=True))
    band_data_sorted, band_label_sorted = zip(*sorted(zip(band_data, band_label), reverse=True))

    statistics = {
        'total_satellites': total_satellites,
        'transmitters': total_transmitters,
        'transmitters_alive': alive_transmitters_percentage,
        'mode_label': mode_label_sorted,
        'mode_data': mode_data_sorted,
        'band_label': band_label_sorted,
        'band_data': band_data_sorted
    }
    return JsonResponse(statistics, safe=False)


@login_required
def users_edit(request):
    """View to render user settings page."""
    token = get_apikey(request.user)
    return render(request, 'base/users_edit.html', {'token': token})
