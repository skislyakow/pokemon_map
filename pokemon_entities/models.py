from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        #return super().__str__()
        return f'{self.title}'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    
    lat = models.FloatField('Lat:')
    lon = models.FloatField('Lon:')

    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время начала события'
    )

    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время окончания события'
    )

