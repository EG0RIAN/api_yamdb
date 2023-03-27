import csv
from reviews.models import GenreTitle


with open('../api_yamdb/static/data/genre_title.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        GenreTitle.objects.create(
            id=row[0],
            tittle_id=row[1],
            genre_id=row[2]
        )
