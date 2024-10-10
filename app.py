from flask import Flask, render_template, request
import random
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Função para carregar os filmes do arquivo XML
def load_movies():
    tree = ET.parse('imdb_top10k.xml')
    root = tree.getroot()
    movies = []
    for row in root.findall('row'):
        title = row.find('Series_Title').text
        year = row.find('Released_Year').text
        director = row.find('Director').text
        image = row.find('Poster_Link').text
        genre = row.find('Genre').text
        rating = row.find('IMDB_Rating').text
        overview = row.find('Overview').text
        movies.append({
            'title': title,
            'year': year,
            'director': director,
            'image': image,
            'genre': genre,
            'rating': float(rating),
            'overview': overview
        })
    return movies

# Função para extrair gêneros únicos do XML
def get_unique_genres(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    genres = set()

    for row in root.findall('row'):
        genre = row.find('Genre').text
        if genre:
            # Divide por vírgula e remove espaços em branco de cada gênero
            for g in genre.split(','):
                genres.add(g.strip().upper())  # Adiciona em letras minúsculas para evitar duplicatas com diferenças de capitalização

    return sorted(genre.strip() for genre in genres)  # Gêneros únicos e ordenados

# Função para aplicar os filtros
def filter_movies(movies, genre_filter, year_filter, rating_filter):
    filtered_movies = movies

    # Filtro por gênero
    if genre_filter:
        filtered_movies = [movie for movie in filtered_movies if genre_filter.lower() in movie['genre'].lower()]

    # Filtro por ano
    if year_filter:
        filtered_movies = [movie for movie in filtered_movies if movie['year'] == year_filter]

    # Filtro por nota (rating)
    if rating_filter == '7':
        filtered_movies = [movie for movie in filtered_movies if 70 <= movie['rating'] < 80]
    elif rating_filter == '8':
        filtered_movies = [movie for movie in filtered_movies if 80 <= movie['rating'] < 90]
    elif rating_filter == '9':
        filtered_movies = [movie for movie in filtered_movies if movie['rating'] >= 90]

    return filtered_movies

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = load_movies()
    genres = get_unique_genres('imdb_top10k.xml')

    genre_filter = request.form.get('genre')
    year_filter = request.form.get('year')
    rating_filter = request.form.get('rating')

    # Aplica os filtros se o formulário for enviado
    if request.method == 'POST':
        filtered_movies = filter_movies(movies, genre_filter, year_filter, rating_filter)
        if filtered_movies:
            random_movie = random.choice(filtered_movies)
        else:
            random_movie = None
    else:
        random_movie = random.choice(movies)

    return render_template('index.html', movie=random_movie, genres=genres, genre_filter=genre_filter, year_filter=year_filter, rating_filter=rating_filter)

if __name__ == '__main__':
    app.run(debug=True)
