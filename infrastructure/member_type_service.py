import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.oracle import db


type = ['gratuit', 'bronze', 'argent', 'or', 'diamond']
prix = [0, 5, 10, 20, 50]
nbr_livre_autorise = [1, 2, 5, 10, 50]

member_type = []
for i in range (0, 4):
    member_type.append((
        type[i],
        prix[i],
        nbr_livre_autorise[i]
    ))

connection = db()
cursor = connection.cursor()

cursor.executemany("""
    INSERT INTO member_type (type, prix, nbr_livre_autorise)
    VALUES (:1, :2, :3)
""", member_type)

connection.commit()
cursor.close()

print(member_type)
        