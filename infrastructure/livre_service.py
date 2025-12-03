import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.oracle import db
import csv
from random import randint


class LivreService():

    def seed_livre_from_csv(self, csv_path, batch_size=500):
        connection = db()
        cursor = connection.cursor()

        batch = []

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                
                batch.append((
                    row['Book-Title'],
                    row['Book-Author'],
                    int(row['Year-Of-Publication']) if row['Year-Of-Publication'].isdigit() else 0,
                    randint(0,20)
                ))

                if len(batch) >= batch_size:
                    self._insert_batch(cursor, batch)
                    batch = []

            if batch:
                self._insert_batch(cursor, batch)

        connection.commit()
        cursor.close()
        connection.close()
        print(f"Seeded books from {csv_path}.")

    def _insert_batch(self, cursor, batch):
        cursor.executemany("""
            INSERT INTO livres (
               titre, auteur, publication_date, stock
            ) VALUES (:1, :2, :3, :4)
        """, batch)

