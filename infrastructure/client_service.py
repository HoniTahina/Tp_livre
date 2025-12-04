import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.oracle import db
import random
from db.oracle import db

class ClientService():
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def gen_name(self):
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

    def gen_num(self):
        start = random.choice(["06", "07"])
        nums = [str(random.randint(0, 9)) for _ in range(8)]
        tel = f"{start}{nums[0]}{nums[1]}{nums[2]}{nums[3]}{nums[4]}{nums[5]}{nums[6]}{nums[7]}"
        return tel

    def gen_email(self, name):
        ext = ['@gmail.com', '@hotmail.fr', 'yahoo.fr']
        name = f"{name}{random.randint(0,99)}"
        name = name.replace(" ", "")
        mail = f"{name}{random.choice(ext)}"
        return mail

    def _insert_client(self, clients):
        self.cursor.executemany("""
            INSERT INTO clients (
               nom, email, tel
            ) VALUES (:1, :2, :3)
        """, clients)

    def seed(self, count=10):
        clients = []
        for _ in range(count):
            name = self.gen_name()
            clients.append((
                name,
                self.gen_email(name),
                self.gen_num()
            ))

        self._insert_client(clients)
        self.conn.commit()
        print(f'✔ Seeded {count} clients')
    
    def creer_utilisateur(self, nom, email, tel=""):
        try:
            self.cursor.execute("""
                INSERT INTO clients (nom, email, tel)
                VALUES (:nom, :email, :tel)
                RETURNING id INTO :new_id
            """, {'nom': nom, 'email': email, 'tel': tel, 'new_id': self.cursor.var(int)})
            
            new_id = self.cursor.bindvars['new_id'].getvalue()[0]
            self.conn.commit()
            return True, new_id, f"Utilisateur créé avec ID: {new_id}"
        except Exception as e:
            self.conn.rollback()
            return False, None, str(e)

    def mettre_a_jour_utilisateur(self, client_id, nom, email, tel):
        try:
            self.cursor.execute("""
                UPDATE clients
                SET nom = :nom, email = :email, tel = :tel
                WHERE id = :client_id
            """, {'nom': nom, 'email': email, 'tel': tel, 'client_id': client_id})
            self.conn.commit()
            return True, "OK"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def tous_les_clients(self):
        self.cursor.execute("""
            SELECT c.id, c.nom, c.email, c.tel,
                   cm.type_id, mt.type, cm.etat,
                   (SELECT COUNT(*) FROM location_livre 
                    WHERE client_id = c.id AND date_retour IS NULL) as active_loans
            FROM clients c
            LEFT JOIN carte_membre cm ON c.id = cm.client_id AND cm.etat = 1
            LEFT JOIN member_type mt ON cm.type_id = mt.id
            ORDER BY c.id DESC
        """)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
