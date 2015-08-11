from shortuuidfield import ShortUUIDField

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


MODE_CHOICES = ['FM', 'AFSK', 'BFSK', 'APRS', 'SSTV', 'CW', 'FMN', 'SSTV', 'GMSK', 'SSB']


class TransmitterApprovedManager(models.Manager):
    def get_queryset(self):
        return super(TransmitterApprovedManager, self).get_queryset().filter(approved=True)


class SuggestionApprovedManager(models.Manager):
    def get_queryset(self):
        return super(SuggestionApprovedManager, self).get_queryset().filter(approved=False)


class Satellite(models.Model):
    """Model for SatNOGS satellites."""
    norad_cat_id = models.PositiveIntegerField()
    name = models.CharField(max_length=45)

    class Meta:
        ordering = ["name"]

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
    mode = models.CharField(choices=zip(MODE_CHOICES, MODE_CHOICES),
                            max_length=10)
    invert = models.BooleanField(default=False)
    baud = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    satellite = models.ForeignKey(Satellite, related_name='transmitters',
                                  null=True)
    approved = models.BooleanField(default=False)

    objects = TransmitterApprovedManager()

    def __unicode__(self):
        return self.description


class Suggestion(Transmitter):
    citation = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.SET_NULL)
    transmitter = models.ForeignKey(Transmitter, blank=True, null=True,
                                    on_delete=models.SET_NULL, related_name='suggestions')

    objects = SuggestionApprovedManager()

    def __unicode__(self):
        return self.description
