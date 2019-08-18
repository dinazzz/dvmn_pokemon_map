from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название на русском')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200, verbose_name='Название на японском')
    image = models.ImageField(blank=True, upload_to='pokemon_img', verbose_name='Изображение')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey('Pokemon', null=True, blank=True, related_name='prev', on_delete=models.SET_NULL, verbose_name='Эволюционировал из')
    next_evolution = models.ForeignKey('Pokemon', null=True, blank=True, related_name='next', on_delete=models.SET_NULL, verbose_name='Эволюционирует в')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(null=True, verbose_name='Широта')
    lon = models.FloatField(null=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='Появился в')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Исчезнет в')
    level = models.IntegerField(null=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title}_{self.id}'