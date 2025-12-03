from db.oracle import db

class EmpruntService:
    def __init__(self):
        self.conn = db()
        self.cursor = self.conn.cursor()

    def peut_emprunter(self, client_id):
        result = self.cursor.callfunc('library_api.can_borrow', int, [client_id])
        return result == 1

    def louer_livre(self, client_id, livre_id):
        try:
            self.cursor.callproc('library_api.rent_book', [client_id, livre_id])
            self.conn.commit()
            return True, "Livre loué avec succès"
        except Exception as e:
            self.conn.rollback()
            error_msg = str(e)
            if 'ORA-20001' in error_msg:
                return False, "Livre indisponible en stock"
            elif 'ORA-20002' in error_msg:
                return False, "Limite de prêt atteinte ou abonnement invalide"
            else:
                return False, f"Erreur : {error_msg}"

    def retourner_livre(self, location_id):
        try:
            self.cursor.callproc('library_api.return_book', [location_id])
            self.conn.commit()
            return True, "Livre retourné avec succès"
        except Exception as e:
            self.conn.rollback()
            return False, f"Erreur : {str(e)}"
