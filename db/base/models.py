from shortuuidfield import ShortUUIDField

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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
    """Model for SatNOGS satellites."""
    norad_cat_id = models.PositiveIntegerField()
    name = models.CharField(max_length=45)
    names = models.TextField(blank=True)
    image = models.ImageField(upload_to='satellites', blank=True,
                              help_text='Ideally: 250x250')

    class Meta:
        ordering = ["name"]

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return settings.SATELLITE_DEFAULT_IMAGE

    @property
    def pending_suggestions(self):
        pending = Suggestion.objects.filter(satellite=self.id).count()
        return pending

    def __unicode__(self):
        return '{0} - {1}'.format(self.norad_cat_id, self.name)


class Transmitter(models.Model):
    uuid = ShortUUIDField(db_index=True, unique=True)
    description = models.TextField()
    alive = models.BooleanField(default=True)
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
    citation = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    transmitter = models.ForeignKey(Transmitter, blank=True, null=True,
                                    on_delete=models.SET_NULL, related_name='suggestions')

    objects = SuggestionApprovedManager()

    def __unicode__(self):
        return self.description
