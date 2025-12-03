INSERT INTO livres(titre, auteur, publication_date, stock)
    VALUES('Sql', 'Paul', '03/12/2025', 100);

INSERT INTO clients(nom, email, tel)
    VALUES ('Honi', 'honi@sql.com', '07070508');

INSERT INTO member_type(type, prix, nbr_livre_autorise)
    VALUES  ("gratuit", 0.0 , 1),
            ("bronze", 5.0, 5);