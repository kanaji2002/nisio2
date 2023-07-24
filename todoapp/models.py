from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_name = models.TextField()
    device_num = models.TextField()
    model_year = models.DateTimeField()
    work_date = models.DateTimeField()
    divA = models.TextField()
    divB = models.TextField()
    disassemble_fig = models.ImageField()
    order_fig = models.ImageField()

    def __str__(self):
        return self.prod_name
        # return self.prod_name

    class Meta:
        ordering = ["prod_name"]
