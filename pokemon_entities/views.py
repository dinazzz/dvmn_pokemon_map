import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    pokemons = Pokemon.objects.filter(id__in=pokemon_entities.values_list('pokemon', flat=True))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.pokemon.image.path)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    next_evolution = requested_pokemon.next_evolution
    previous_evolution = requested_pokemon.previous_evolution

    if next_evolution is not None:
        next_evolution = {
            "title_ru": requested_pokemon.next_evolution.title,
            "pokemon_id": requested_pokemon.next_evolution.id,
            "img_url": requested_pokemon.next_evolution.image.url
        }
    if previous_evolution is not None:
        previous_evolution = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": requested_pokemon.previous_evolution.image.url
        }

    pokemon_info = {
        'pokemon_id': pokemon_id,
        'img_url': requested_pokemon.image.url,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'next_evolution': next_evolution,
        'previous_evolution': previous_evolution
    }
    requested_pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_entity.pokemon.image.path)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_info})
