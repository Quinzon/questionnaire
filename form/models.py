from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, blank=True, null=True)
    struct = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    email = models.EmailField()
    answer = models.JSONField(blank=True, null=True)
