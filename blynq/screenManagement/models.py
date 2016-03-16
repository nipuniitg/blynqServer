from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Group(models.Model):
    group_name = models.CharField(max_length=100,null= False)
    created_on = models.DateField()
    description = models.CharField(max_length=500)

    def __unicode__(self):
        return self.group_name

    def _get_group_screens(id):
        return Screen.Objects.all(group_id = id)

class Screen(models.Model):
    Screen_Sizes=(
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
    )
    screen_id = models.AutoField(primary_key=True)
    activated_on = models.DateField()
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=100, null=False)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    screen_size = models.CharField(max_length=1, choices=Screen_Sizes)
    activation_key = models.CharField(max_length=16)

    def __unicode__(self):
        return self.screen_name



