from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
from movie.models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name':'Martin Betancur'})
    searchTerm = request.GET.get('searchMovie', '')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    return render(request, 'about.html')


def signup(request):
    email = request.GET.get('email')  
    return render(request, 'signup.html', {'email':email})


def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    # Ajustar el espacio entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica de películas por año a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica de películas por año
    return render(request, 'statistics.html', {'graphic': graphic})


def movie_genre_chart(request):
    # Obtener todas las películas
    movies = Movie.objects.all()

    # Crear un diccionario para contar la cantidad de películas por género
    genre_count = {}
    for movie in movies:
        # Obtener el primer género de la película
        genre = movie.genre.split(',')[0].strip()
        # Incrementar el contador para ese género
        genre_count[genre] = genre_count.get(genre, 0) + 1

    # Preparar los datos para la gráfica
    genres = list(genre_count.keys())
    counts = list(genre_count.values())

    # Crear la gráfica
    plt.bar(genres, counts)
    plt.xlabel('Género')
    plt.ylabel('Cantidad de Películas')
    plt.title('Cantidad de Películas por Género')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    chart = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con la gráfica
    return render(request, 'movie_genre_chart.html', {'chart': chart})
