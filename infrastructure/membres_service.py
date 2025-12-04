from db.oracle import db
from datetime import datetime

class ServiceMembre:
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def info_membre(self, client_id):
        self.cursor.execute("""
            SELECT c.id, c.nom, c.email, 
                   cm.type_id, mt.type, mt.nbr_livre_autorise,
                   cm.etat
            FROM clients c
            LEFT JOIN carte_membre cm ON c.id = cm.client_id
            LEFT JOIN member_type mt ON cm.type_id = mt.id
            WHERE c.id = :client_id
        """, {'client_id': client_id})
        return self.cursor.fetchone()

    def creer_carte_membre(self, client_id, type_id=1):
        try:
            now = datetime.now()
            self.cursor.execute("""
                SELECT COUNT(*) FROM carte_membre 
                WHERE client_id = :client_id AND etat = 1
            """, {'client_id': client_id})
            if self.cursor.fetchone()[0] > 0:
                return False, "Le client possède déjà une carte active"

            self.cursor.execute("""
                INSERT INTO carte_membre (date_creation, client_id, type_id, etat)
                VALUES (:date_creation, :client_id, :type_id, 1)
            """, {'date_creation': now,'client_id': client_id, 'type_id': type_id})

            self.conn.commit()
            return True, "Carte membre créée"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def desactiver_carte_membre(self, client_id):
        try:
            self.cursor.execute("""
                UPDATE carte_membre
                SET etat = 0
                WHERE client_id = :client_id AND etat = 1
            """, {'client_id': client_id})

            self.conn.commit()
            return True, "Carte membre désactivée"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def types_membre(self):
        self.cursor.execute("""
            SELECT id, type, prix, nbr_livre_autorise
            FROM member_type
            ORDER BY id
        """)
        return self.cursor.fetchall()

    def ajouter_type_membre(self, type_name, prix, nbr_livre_autorise):
        try:
            self.cursor.execute("""
                INSERT INTO member_type (type, prix, nbr_livre_autorise)
                VALUES (:type_name, :prix, :nbr_livre_autorise)
            """, {'type_name': type_name, 'prix': prix, 'nbr_livre_autorise': nbr_livre_autorise})
            self.conn.commit()
            return True, "Type de membre ajouté"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def modifier_type_membre(self, type_id, type_name, prix, nbr_livre_autorise):
        try:
            self.cursor.execute("""
                UPDATE member_type
                SET type = :type_name, prix = :prix, nbr_livre_autorise = :nbr
                WHERE id = :type_id
            """, {'type_name': type_name, 'prix': prix, 'nbr': nbr_livre_autorise, 'type_id': type_id})
            self.conn.commit()
            return True, "Type de membre modifié"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def supprimer_type_membre(self, type_id):
        try:
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM carte_membre 
                WHERE type_id = :type_id AND etat = 1
            """, {'type_id': type_id})
            
            if self.cursor.fetchone()[0] > 0:
                return False, "Impossible de supprimer : des membres utilisent ce type actif"

            self.cursor.execute("""
                DELETE FROM member_type 
                WHERE id = :type_id
            """, {'type_id': type_id})
            
            self.conn.commit()
            return True, "Type de membre supprimé"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)