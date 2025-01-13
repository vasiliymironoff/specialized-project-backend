from django.db import models

class NewsData(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=255)
    path_audio = models.CharField(max_length=255)

    class Meta:
        db_table = 'news'
