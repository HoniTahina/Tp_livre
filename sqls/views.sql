CREATE OR REPLACE VIEW v_membres_actifs AS
SELECT c.id, c.nom, c.email, cm.type_id, mt.type, cm.etat
FROM clients c
JOIN carte_membre cm ON c.id = cm.client_id
JOIN member_type mt ON cm.type_id = mt.id
WHERE cm.etat = 1;

CREATE OR REPLACE VIEW v_books_borrowed AS
SELECT c.id AS client_id,
       c.nom,
       COUNT(l.id) AS livre_count
FROM clients c
LEFT JOIN location_livre l ON c.id = l.client_id
GROUP BY c.id, c.nom;

CREATE OR REPLACE VIEW v_loans_in_progress AS
SELECT l.*, li.titre, c.nom, c.email
FROM location_livre l
JOIN livres li ON li.id = l.livre_id
JOIN clients c ON c.id = l.client_id
WHERE l.date_retour IS NULL;

CREATE OR REPLACE VIEW v_top_livres AS
SELECT li.id, li.titre, COUNT(*) AS borrow_count
FROM location_livre l
JOIN livres li ON li.id = l.livre_id
GROUP BY li.id, li.titre
ORDER BY borrow_count DESC;
