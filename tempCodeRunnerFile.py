from flask import Flask, render_template
import random
import xml.etree.ElementTree as ET

app = Flask(__name__)

def load_movies():
    tree = ET.parse('imdb_top_1000.xml')
    root = tree.getroot()
    movies = []
    for row in root.findall('row'):
        title = row.find('Series_Title').text
        year = row.find('Released_Year').text
        director = row.find('Director').text
        image = row.find('Poster_Link').text
        overview = row.find('Overview').text
        movies.append({'title': title, 'year': year, 'director': director, 'image': image, 'overview': overview})
    return movies

@app.route('/')
def index():
    movies = load_movies()
    random_movie = random.choice(movies)
    return render_template('index.html', movie=random_movie)

if __name__ == '__main__':
    app.run(debug=True)
