from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'groups'