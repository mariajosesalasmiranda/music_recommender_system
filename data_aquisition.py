import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# --- Configuration ---
CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "1d0daa19164b4982aa37fa577ead8bdc") 
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "cb34766250664b1eb9ba037375439b84") 

# --- Setup Function ---
def get_spotify_client():
    """Initializes and returns the Spotipy client."""
    if not CLIENT_ID or not CLIENT_SECRET or CLIENT_ID == "YOUR_CLIENT_ID":
        print("🚨 Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables or update the script.")
        return None
        
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

# --- Data Fetching Function ---
def fetch_track_features(track_ids):
    """
    Fetches audio features for a list of track IDs.

    :param track_ids: A list of Spotify track IDs (strings).
    :return: A pandas DataFrame with the track features.
    """
    sp = get_spotify_client()
    if sp is None:
        return pd.DataFrame()

    print(f"Fetching features for {len(track_ids)} tracks...")
    
    # Spotify API limits fetching to 50 tracks per request
    features_list = []
    chunk_size = 50
    for i in range(0, len(track_ids), chunk_size):
        chunk = track_ids[i:i + chunk_size]
        try:
            # Get audio features
            features = sp.audio_features(chunk)
            # Filter out None results (if a track ID is invalid)
            features_list.extend([f for f in features if f is not None])
        except Exception as e:
            print(f"An error occurred while fetching a chunk: {e}")
            
    if not features_list:
        print("No features were fetched successfully.")
        return pd.DataFrame()
        
    # Convert the list of feature dictionaries to a DataFrame
    df_features = pd.DataFrame(features_list)
    # Select and rename columns for clarity
    feature_cols = [
        'id', 'danceability', 'energy', 'key', 'loudness', 'mode', 
        'speechiness', 'acousticness', 'instrumentalness', 'liveness', 
        'valence', 'tempo', 'duration_ms', 'time_signature'
    ]
    return df_features[feature_cols]

# --- Example Usage ---
if __name__ == '__main__':
    # Example track IDs for popular songs
    example_track_ids = [
        '2P8cBL9d9h2F6mK5w4vE0r', # Blinding Lights - The Weeknd
        '0VjIjW4GlUZ3BdoCvKINaU', # As It Was - Harry Styles
        '6L0ADU5QyI3N1i8g5F92zL', # Heat Waves - Glass Animals
    ]
    
    features_df = fetch_track_features(example_track_ids)
    
    if not features_df.empty:
        print("\n--- Fetched Track Features (Head) ---")
        print(features_df.head())
        print(f"\nDataFrame shape: {features_df.shape}")