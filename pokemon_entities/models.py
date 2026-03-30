from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        #return super().__str__()
        return f'{self.title}'