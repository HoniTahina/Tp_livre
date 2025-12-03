from db.oracle import db

class ViewsService:
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def membres_actifs(self):
        self.cursor.execute("""
            SELECT id, nom, email, type_id, type, etat
            FROM v_membres_actifs
        """)
        return self.cursor.fetchall()

    def livres_empruntes_par_client(self):
        self.cursor.execute("""
            SELECT client_id, nom, livre_count
            FROM v_books_borrowed
            ORDER BY livre_count DESC
        """)
        return self.cursor.fetchall()

    def emprunts_en_cours(self):
        self.cursor.execute("""
            SELECT id, livre_id, client_id, titre, nom, email, date_sortie
            FROM v_loans_in_progress
            ORDER BY date_sortie DESC
        """)
        return self.cursor.fetchall()

    def meilleurs_livres(self, limite=10):
        self.cursor.execute(f"""
            SELECT * FROM (
                SELECT id, titre, borrow_count
                FROM v_top_livres
            ) WHERE ROWNUM <= {limite}
        """)
        return self.cursor.fetchall()
