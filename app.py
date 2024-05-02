from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# Function to clean up movie title (lowercase and strip spaces)
def clean_movie_title(movie_title):
    return movie_title.lower().strip()

# Function for movie recommendation
def recommend_movies(movie_title, similarity_matrix, movie_list, n):
    cleaned_title = clean_movie_title(movie_title)
    
    # Find index of the cleaned movie title in the movie list
    movie_index = None
    for i, title in enumerate(movie_list):
        if clean_movie_title(title) == cleaned_title:
            movie_index = i
            break
    
    if movie_index is None:
        return None  # Movie title not found

    # Get similarity scores for the given movie index
    similarity_scores = similarity_matrix[movie_index]

    # Sort indices based on similarity scores (higher similarity first)
    similar_movie_indices = sorted(
        list(enumerate(similarity_scores)), reverse=True, key=lambda x: x[1]
    )[1 : n + 1]  # Exclude the input movie itself

    # Get top similar movie titles
    recommended_movies = []
    for idx, score in similar_movie_indices:
        recommended_movies.append(movie_list[idx])

    return recommended_movies


# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle movie recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        recommended_movies = recommend_movies(movie_title, similarity_matrix, movie_list, 5)
        
        if recommended_movies is None:
            error_message = "Movie not found. Please try a different title."
            return render_template('index.html', error_message=error_message)
        
        return render_template('recommendations.html', movie_title=movie_title, recommended_movies=recommended_movies)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
