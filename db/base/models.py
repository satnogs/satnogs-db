from os import path
from shortuuidfield import ShortUUIDField
from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

from db.base.helpers import gridsquare

DATA_SOURCES = ['manual', 'network', 'sids']


def _name_payload_frame(instance, filename):
    folder = 'payload_frames'
    ext = 'raw'
    filename = '{0}_{1}.{2}'.format(filename, uuid4().hex, ext)
    return path.join(folder, filename)


def _gen_observer(sender, instance, created, **kwargs):
    post_save.disconnect(_gen_observer, sender=DemodData)
    try:
        qth = gridsquare(instance.lat, instance.lng)
    except:
        instance.observer = 'Unknown'
    else:
        instance.observer = '{0}-{1}'.format(instance.station, qth)
    instance.save()
    post_save.connect(_gen_observer, sender=DemodData)


class TransmitterApprovedManager(models.Manager):
    def get_queryset(self):
        return super(TransmitterApprovedManager, self).get_queryset().filter(approved=True)


class SuggestionApprovedManager(models.Manager):
    def get_queryset(self):
        return super(SuggestionApprovedManager, self).get_queryset().filter(approved=False)


class Mode(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.name


class Satellite(models.Model):
    """Model for all the satellites."""
    norad_cat_id = models.PositiveIntegerField()
    name = models.CharField(max_length=45)
    names = models.TextField(blank=True)
    image = models.ImageField(upload_to='satellites', blank=True,
                              help_text='Ideally: 250x250')
    tle1 = models.CharField(max_length=200, blank=True)
    tle2 = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['norad_cat_id']

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.SATELLITE_DEFAULT_IMAGE

    @property
    def pending_suggestions(self):
        pending = Suggestion.objects.filter(satellite=self.id).count()
        return pending

    @property
    def has_telemetry_data(self):
        has_data = DemodData.objects.filter(satellite=self.id).count()
        return has_data

    @property
    def has_telemetry_decoders(self):
        has_decoders = Telemetry.objects.filter(satellite=self.id).exclude(decoder='').count()
        return has_decoders

    def __unicode__(self):
        return '{0} - {1}'.format(self.norad_cat_id, self.name)


class Transmitter(models.Model):
    """Model for satellite transmitters."""
    uuid = ShortUUIDField(db_index=True, unique=True)
    description = models.TextField()
    alive = models.BooleanField(default=True)
    ALIVE = 'a'
    DEAD = 'd'
    RE_ENTERED = 'r'
    STATUS = (
        (ALIVE, 'Alive'),
        (DEAD, 'Dead'),
        (RE_ENTERED, 'Re-entered'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ALIVE,
    )
    uplink_low = models.PositiveIntegerField(blank=True, null=True)
    uplink_high = models.PositiveIntegerField(blank=True, null=True)
    downlink_low = models.PositiveIntegerField(blank=True, null=True)
    downlink_high = models.PositiveIntegerField(blank=True, null=True)
    mode = models.ForeignKey(Mode, blank=True, null=True,
                             on_delete=models.SET_NULL, related_name='transmitters')
    invert = models.BooleanField(default=False)
    baud = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    satellite = models.ForeignKey(Satellite, related_name='transmitters',
                                  null=True)
    approved = models.BooleanField(default=False)

    objects = TransmitterApprovedManager()

    def __unicode__(self):
        return self.description

    def update_from_suggestion(self, suggestion):
        self.description = suggestion.description
        self.alive = suggestion.alive
        self.downlink_low = suggestion.downlink_low
        self.downlink_high = suggestion.downlink_high
        self.uplink_low = suggestion.uplink_low
        self.uplink_high = suggestion.uplink_high
        self.mode = suggestion.mode
        self.invert = suggestion.invert
        self.baud = suggestion.baud
        self.approved = True
        self.save()


class Suggestion(Transmitter):
    """Model for transmitter suggestions."""
    citation = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    transmitter = models.ForeignKey(Transmitter, blank=True, null=True,
                                    on_delete=models.SET_NULL, related_name='suggestions')

    objects = SuggestionApprovedManager()

    def __unicode__(self):
        return self.description


class Telemetry(models.Model):
    """Model for satellite telemtry decoders."""
    satellite = models.ForeignKey(Satellite, null=True, related_name='telemetries')
    name = models.CharField(max_length=45)
    schema = models.TextField(blank=True)
    decoder = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['satellite__norad_cat_id']
        verbose_name_plural = 'Telemetries'

    def __unicode__(self):
        return self.name


class DemodData(models.Model):
    """Model for satellite for observation data."""
    satellite = models.ForeignKey(Satellite, null=True, related_name='telemetry_data')
    transmitter = models.ForeignKey(Transmitter, null=True, blank=True)
    source = models.CharField(choices=zip(DATA_SOURCES, DATA_SOURCES),
                              max_length=7, default='sids')
    data_id = models.PositiveIntegerField(blank=True, null=True)
    payload_frame = models.FileField(upload_to=_name_payload_frame, blank=True, null=True)
    payload_decoded = models.TextField(blank=True)
    payload_telemetry = models.ForeignKey(Telemetry, null=True, blank=True)
    station = models.CharField(max_length=45, default='Unknown')
    observer = models.CharField(max_length=60, blank=True)
    lat = models.FloatField(validators=[MaxValueValidator(90), MinValueValidator(-90)],
                            default=0)
    lng = models.FloatField(validators=[MaxValueValidator(180), MinValueValidator(-180)],
                            default=0)
    timestamp = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return 'data-for-{0}'.format(self.satellite.norad_cat_id)

    def display_frame(self):
        with open(self.payload_frame.path) as fp:
            return fp.read()


post_save.connect(_gen_observer, sender=DemodData)
