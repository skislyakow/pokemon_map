import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon
from .models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon(folium_map, lat, lon, image_url):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = timezone.now()

    active_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    ).select_related('pokemon')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in active_entities:
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
            'img_url': pokemon.image.url,
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
    now = timezone.now()
    active_entities = pokemon.entities.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )
    for entity in active_entities:
        img_url = request.build_absolute_uri(pokemon.image.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            img_url
        )

    next_pokemon = pokemon.next_evolution
    if pokemon.next_evolution:
        next_evolution = {
            'pokemon_id': next_pokemon.id,
            'title_ru': next_pokemon.title,
            'img_url': request.build_absolute_uri(next_pokemon.image.url),
        }
    else:
        next_evolution = None

    previous_pokemon = pokemon.previous_evolutions.first()
    if previous_pokemon:
        previous_evolution = {
            'pokemon_id': previous_pokemon.id,
            'title_ru': previous_pokemon.title,
            'img_url': request.build_absolute_uri(previous_pokemon.image.url),
        }
    else:
        previous_evolution = None

    pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
            'description': pokemon.description,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'next_evolution': next_evolution,
            'previous_evolution': previous_evolution
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page
    })
