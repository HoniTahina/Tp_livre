from db.oracle import db

class LivresRechercheService:
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def rechercher_livres(self, recherche="", limite=50):
        query = """
            SELECT id, titre, auteur, publication_date, stock
            FROM livres
            WHERE UPPER(titre) LIKE UPPER(:search) 
               OR UPPER(auteur) LIKE UPPER(:search)
            ORDER BY titre
            FETCH FIRST :limit ROWS ONLY
        """
        self.cursor.execute(query, {
            'search': f'%{recherche}%',
            'limit': limite
        })
        return self.cursor.fetchall()
