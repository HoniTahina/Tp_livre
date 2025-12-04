from db.oracle import db

class StatsEmpruntsService:
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def emprunts_client(self, client_id):
        self.cursor.execute("""
            SELECT l.id, l.livre_id, li.titre, l.date_sortie, l.date_retour
            FROM location_livre l
            JOIN livres li ON li.id = l.livre_id
            WHERE l.client_id = :client_id
            ORDER BY l.date_sortie DESC
        """, {'client_id': client_id})
        return self.cursor.fetchall()

    def historique_emprunts(self, client_id):
        self.cursor.execute("""
            SELECT l.id, li.titre, li.auteur, l.date_sortie, l.date_retour,
                   CASE 
                       WHEN l.date_retour IS NULL THEN 'Actif'
                       ELSE 'Retourné'
                   END as status
            FROM location_livre l
            JOIN livres li ON li.id = l.livre_id
            WHERE l.client_id = :client_id
            ORDER BY l.date_sortie DESC
        """, {'client_id': client_id})
        return self.cursor.fetchall()
