import pickle
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load your existing movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Your TMDB API key
api_key = "ca47a983c66a5855319b070afcaf393e"

def get_poster_url(movie_title):
    """Fetch poster URL from TMDB for a given movie title."""
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": api_key, "query": movie_title}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

        # If no poster found
        return "https://via.placeholder.com/500x750.png?text=No+Image"

    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# Dictionary to store poster URLs
posters = {}

# Use ThreadPoolExecutor to speed up API calls
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(get_poster_url, title): title for title in movies['title']}

    for count, future in enumerate(as_completed(futures), 1):
        title = futures[future]
        try:
            poster_url = future.result()
            posters[title] = poster_url
            print(f" [{count}/{len(movies)}] {title} -> {poster_url}")
        except Exception as e:
            print(f" Error for {title}: {e}")
            posters[title] = "https://via.placeholder.com/500x750.png?text=No+Image"

# Add poster URLs to DataFrame
movies['poster'] = movies['title'].map(posters)

# Save the updated data
with open('movie_dict_with_posters.pkl', 'wb') as f:
    pickle.dump(movies.to_dict(), f)

print("All posters added and saved to movie_dict_with_posters.pkl")
