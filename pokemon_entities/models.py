from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
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

    level = models.IntegerField('Уровень:', null=True, blank=True)
    health = models.IntegerField('Здоровье:', null=True, blank=True)
    strength = models.IntegerField('Атака:', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title, self.level}'