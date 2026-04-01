import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon
from .models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
NOW_UTC = timezone.now()


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        if entity.disappeared_at and entity.disappeared_at > NOW_UTC > entity.appeared_at:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)

            add_pokemon(
                folium_map,
                entity.lat,
                entity.lon,
                img_url
            )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    for entity in pokemon_entities:
        img_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url
        )

    next_evolution = None
    next_evolution = getattr(pokemon, 'next_evolution', None)
    
    if next_evolution:
        try:
            next_evolution = {
                'pokemon_id': next_evolution.id,
                'title_ru': next_evolution.title,
                'img_url': request.build_absolute_uri(next_evolution.image.url) if next_evolution.image else DEFAULT_IMAGE_URL
            }
        except Exception:
            next_evolution = None

    previous_evolution = None
    previous_evolution = Pokemon.objects.filter(next_evolution=pokemon).first()
    
    if previous_evolution:
        previous_evolution = {
            'pokemon_id': previous_evolution.id,
            'title_ru': previous_evolution.title,
            'img_url': request.build_absolute_uri(previous_evolution.image.url) if previous_evolution.image else DEFAULT_IMAGE_URL
        }

    pokemons_on_page = [{
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'next_evolution': next_evolution,
            'previous_evolution': previous_evolution
        }]
    

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemons_on_page[0]
    })
