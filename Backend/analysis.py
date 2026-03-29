import pandas as pd
from pathlib import Path
import gender_guesser.detector as gender_detector

gd = gender_detector.Detector(case_sensitive=False)

def guess_gender(full_name):
    first = full_name.strip().split()[0]
    result = gd.get_gender(first)
   
    if result == 'female' or result == 'mostly_female':
        return 'female'
    if result == 'male' or result == 'mostly_male':
        return 'male'
    return 'unknown'  


BASE = Path(__file__).parent.parent   
DATA = BASE / "Data"                 
FRONTEND = BASE / "Frontend"

basics = pd.read_csv(
    DATA / "title.basics.tsv.gz",
    sep='\t',
    low_memory=False,
    na_values='\\N',
    usecols=['tconst', 'titleType', 'primaryTitle', 'startYear', 'genres']
)

print("Loading ratings...")
ratings = pd.read_csv(
    DATA / "title.ratings.tsv.gz",
    sep='\t',
    low_memory=False,
    na_values='\\N',
    usecols=['tconst', 'averageRating', 'numVotes']
)

print("Loading crew...")
crew = pd.read_csv(
    DATA / "title.crew.tsv.gz",
    sep='\t',
    low_memory=False,
    na_values='\\N',
    usecols=['tconst', 'directors']
)

print("Loading names...")
names = pd.read_csv(
    DATA / "name.basics.tsv.gz",
    sep='\t',
    low_memory=False,
    na_values='\\N',
    usecols=['nconst', 'primaryName']
)

basics = basics[basics['titleType'] == 'movie'].copy()

basics = basics.dropna(subset=['startYear'])
basics['startYear'] = basics['startYear'].astype(int)
basics = basics[basics['startYear'] >= 1990]

ratings = ratings[ratings['numVotes'] >= 500].copy()

crew = crew.dropna(subset=['directors']).copy()

print(f"  basics after filter:  {len(basics):,} movies")
print(f"  ratings after filter: {len(ratings):,} entries")

df = basics.merge(ratings, on='tconst')
df = df.merge(crew[['tconst', 'directors']], on='tconst')

print(f"  after merging ratings + crew: {len(df):,} rows")

df['directors'] = df['directors'].str.split(',')
df = df.explode('directors')
df = df.dropna(subset=['directors'])
df['directors'] = df['directors'].str.strip()

df = df.merge(names, left_on='directors', right_on='nconst', how='left')
df = df.dropna(subset=['primaryName'])

print("Inferring gender...")
df['director_gender'] = df['primaryName'].apply(guess_gender)

gender_counts = df['director_gender'].value_counts()
print(f"  female: {gender_counts.get('female',0):,}")
print(f"  male:   {gender_counts.get('male',0):,}")
print(f"  unknown:{gender_counts.get('unknown',0):,}")

# Drop unknowns — ambiguous labels hurt the analysis
df = df[df['director_gender'] != 'unknown'].copy()


gender_per_film = df.groupby('tconst')['director_gender'].nunique()
solo_directed = gender_per_film[gender_per_film == 1].index
df = df[df['tconst'].isin(solo_directed)].copy()

df = df.drop_duplicates(subset='tconst').copy()

print(f"  films after dropping co-directed + unknowns: {len(df):,}")

df = df.dropna(subset=['averageRating', 'genres']).copy()

df = df.rename(columns={
    'primaryTitle':    'title',
    'startYear':       'year',
    'genres':          'genre',
    'averageRating':   'rating',
    'numVotes':        'votes',
    'director_gender': 'gender',
    'primaryName':     'director'
})

df['genre'] = df['genre'].str.split(',').str[0]

df = df[['title', 'year', 'genre', 'gender', 'rating', 'votes', 'director']]
df = df.sort_values('votes', ascending=False).reset_index(drop=True)

print("\n── Sanity check ")
print(f"Total films:  {len(df):,}")
print(df['gender'].value_counts().to_string())
print(f"\nMean rating (female): {df[df['gender']=='female']['rating'].mean():.3f}")
print(f"Mean rating (male):   {df[df['gender']=='male']['rating'].mean():.3f}")
print(f"\nYear range: {df['year'].min()} – {df['year'].max()}")
print(f"Top genres:\n{df['genre'].value_counts().head(8).to_string()}")
print("──────────────────────────────────────────\n")

out_csv  = BASE / "Backend" / "movies_clean.csv"
out_json = FRONTEND / "real_data.json"

df.to_csv(out_csv, index=False)
print(f"CSV saved  → {out_csv}")

df.to_json(out_json, orient='records', indent=2)
print(f"JSON saved → {out_json}")