#!/usr/bin/env python3

import cgi
import cgitb
import pickle
import pandas as pd
import requests

cgitb.enable()  # Enable debugging

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load the data
movies = pd.DataFrame(pickle.load(open('/path/to/movie_dict.pkl', 'rb')))
similarity = pickle.load(open('/path/to/similarity.pkl', 'rb'))

# Get data from the form
form = cgi.FieldStorage()
selected_movie = form.getvalue('movie')

# Generate the recommendations
if selected_movie:
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
else:
    recommended_movie_names = []
    recommended_movie_posters = []

# Print the HTML response
print("Content-Type: text/html")
print()
print("<html><head>")
print("<title>Movie Recommender System</title>")
print("</head><body>")
print("<h1>Movie Recommender System</h1>")
print("<form method='post' action='/cgi-bin/movie_recommendation.py'>")
print("<label for='movie'>Select a movie:</label>")
print("<select name='movie' id='movie'>")

# Populate the dropdown with movie titles
for title in movies['title']:
    print(f"<option value='{title}'>{title}</option>")

print("</select>")
print("<input type='submit' value='Show Recommendation'>")
print("</form>")

# Display the recommendations
if recommended_movie_names:
    print("<h2>Recommended Movies:</h2>")
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        print(f"<div style='display:inline-block;margin-right:20px;'>")
        print(f"<p>{name}</p>")
        print(f"<img src='{poster}' width='150'>")
        print("</div>")

print("</body></html>")
