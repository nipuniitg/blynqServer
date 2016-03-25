from django.db import models

# Create your models here.
from authentication.models import UserDetails


class ContentType(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('IMG', 'Image'),
        # Uncomment below types when we add support
        ('VID', 'Video'),
        ('PPT', 'Presentation'),
        ('GIF', 'Gif'),
    )
    type = models.CharField(max_length=3, choices=CONTENT_TYPE_CHOICES)
    fileExtension = models.CharField(max_length=5)


class Content(models.Model):
    title = models.CharField(max_length=100)
    # filename is generated from the title and the file-extension
    # filename should also handle spaces
    filename = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_uploaded_by')
    last_modified_by = models.ForeignKey(UserDetails, on_delete=models.PROTECT, related_name='%(class)s_modified_by')
    last_modified_time = models.DateTimeField()
    is_folder = models.BooleanField()
    file_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    # directory_path is the location of the folder on the server where the current
    # file/ directory is uploaded to. This should contain a trailing /
    # For example, /user/nipun/docs/
    directory_path = models.CharField(max_length=300)

    def full_file_path(self):
        return self.directory_path + self.filename

