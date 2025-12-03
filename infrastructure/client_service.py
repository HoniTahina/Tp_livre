import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.oracle import db
import random


class ClientService():
    
    def gen_name():
        tab_name =['Dupond','Joe','Marie','Sophie','Martin','Lucas','Emma','Paul','Lina','Adam',
        'Chloe','Noah','Lea','Hugo','Nina','Thomas','Eva','Yanis','Sarah','Leo',
        'Julie','Omar','Clara','Moussa','Victor','Amina','Bastien','Ines','Kylian',
        'Maya','Arthur','Alice','Ibrahim','Nora','Jules','Camille','Rayan','Laura',
        'Antoine','Sabrina','Walid','Alicia','Maxime','Elena','Karim','Sarah2','Amadou',
        'Lucie','Dylan','Mael','Fatou','Theo','Anais','Mohamed','Jade','Ilyes','Mila',
        'Raphael','Nadia','Samuel','Kenza','Alex','Lola','Nicolas','Mariama','Jordan',
        'Melissa','Gabriel','Sira','Quentin','Oceane','Brahim','Eva2','Remy','Sami',
        'Adama','Sonia','Axel','Helena','Ismael','Julie2','Kevin','Nassima','Rita',
        'Ousmane','Yasmine','Cedric','Tania','Patrick','Hawa','Florian','Dalila',
        'Celine','Abdou','Coralie','Mamoudou','Rokia','Etienne','Salimata','Bruno'
        ]
        tab_firstname = ['Adele','Benoit','Caroline','Didier','Emilie','Fabrice','Gerald','Helene','Isabelle','Jean',
        'Katia','Laurent','Manon','Nadine','Olivier','Patricia','Quentin','Roland','Sandrine','Thierry',
        'Ulysse','Valerie','William','Xavier','Yohan','Zoé','Abel','Brigitte','Clement','Doria',
        'Elie','Fatima','Gaston','Hafsa','Iris','Johan','Kenza2','Leopold','Mireille','Nils',
        'Oceane2','Pierre','Quitterie','Remi','Selma','Tarek','Ursule','Violette','Warren','Xena',
        'Yasmine2','Zacharie','Aminata','Bilal','Corinne','Demba','Ethan','Farah','Gaetan','Hana',
        'Ibrahim2','Josue','Kilian','Louise','Mohamed2','Naila','Oumar','Prisca','Reda','Sidy',
        'Tania2','Umar','Vanessa','Waly','Xiomara','Yvan','Zoumana','Abdoul','Bocar','Chantal',
        'Djibril','Elina','Fodie','Ghislaine','Habib','Imane','Jalil','Khadija','Lamine','Moussa2',
        'Noura','Oualid','Penda','Rokhaya','Souleymane','Tidiane','Ugo','Viviane','Wassim','Yara'
        ]
        name = (f"{random.choice(tab_name)} {random.choice(tab_firstname)}")
        return name

    def gen_num():
        start = random.choice(["06", "07"])
        nums = [str(random.randint(0, 9)) for _ in range(8)]
        tel = f"{start}{nums[0]}{nums[1]}{nums[2]}{nums[3]}{nums[4]}{nums[5]}{nums[6]}{nums[7]}"
        return tel

    def gen_email(name):
        ext = ['@gmail.com', '@hotmail.fr', 'yahoo.fr']
        name = f"{name}{random.randint(0,99)}"
        name = name.replace(" ", "")
        mail = f"{name}{random.choice(ext)}"
        return mail

    def insert (self, clients):
        connection = db()
        cursor = connection.cursor()
        self._insert_client(cursor, clients)
        print('insertion success')
        connection.commit()
        cursor.close()
        connection.close()

    def _insert_client(self, cursor, client):
        cursor.executemany("""
            INSERT INTO clients (
               nom, email, tel
            ) VALUES (:1, :2, :3)
        """, client)

    clients = []
    for i in range(0,2):
        name = gen_name()
        clients.append((
            name,
            gen_email(name),
            gen_num()
        ))
    print (clients)
    

 
