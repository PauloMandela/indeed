from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField("Native name", max_length=200)
    latinletter = models.CharField("Latin name first letter", max_length=2, default="")
    banned = models.BooleanField("Banned?", default=False)

    def __str__(self):
        return self.name
    
    def serializeCustom(self):
        data = {
            "id": self.pk,
            "name": self.name,
            "letter": self.latinletter,
            "ban" : self.banned,
        }
        return data