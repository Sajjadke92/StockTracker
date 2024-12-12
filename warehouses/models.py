from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200,blank=True)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.title)

class Item(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    quantity = models.IntegerField()
    expiry = models.DateField()
    updated_time = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)