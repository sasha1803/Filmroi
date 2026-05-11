import pandas as pd
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context
DATA = os.path.expanduser('~/Documents/FilmROI/data/')

print("Downloading real movie dataset from GitHub...")
url = "https://raw.githubusercontent.com/danielgrijalva/movie-stats/master/movies.csv"
df = pd.read_csv(url)
df.to_csv(DATA + 'movies.csv', index=False)
print(f"Done! {len(df)} movies saved")
print(f"Columns: {df.columns.tolist()}")
