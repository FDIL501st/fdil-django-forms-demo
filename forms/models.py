from django.db import models


# Create your models here.


class ReportForm(models.Model):
    """A form that is filled out by a user to report something."""

    class Location(models.TextChoices):
        """Possible locations for reporting."""
        OFFICE = "office", 'Office'
        LOUNGE = "lounge", 'Lounge'
        PARKINGLOT = "parkinglot", 'Parking lot'
        WORKSPACE1 = "workspace1", 'WorkSpace1'
        WORKSPACE2 = "workspace2", 'WorkSpace2'
        WORKSPACE3 = "workspace3", 'WorkSpace3'

    name = models.CharField(max_length=100)
    date = models.DateField()
    what = models.TextField()
    where = models.CharField(choices=Location)
    reason = models.TextField()

    def __str__(self):
        return self.name
