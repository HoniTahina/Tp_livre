CREATE OR REPLACE PACKAGE library_api AS

    FUNCTION can_borrow(
        p_client IN NUMBER
    ) RETURN NUMBER;

    PROCEDURE rent_book(
        p_client IN NUMBER,
        p_livre IN NUMBER
    );

    PROCEDURE return_book(
        p_location_id IN NUMBER
    );

END library_api;
/

CREATE OR REPLACE PACKAGE BODY library_api AS

-------------------------------------------------
-- FUNCTION: check if user can borrow a book
-------------------------------------------------
FUNCTION can_borrow(
    p_client IN NUMBER
) RETURN NUMBER
IS
    v_type_id NUMBER;
    v_allowed NUMBER;
    v_current NUMBER;
BEGIN
    -- Get membership type
    SELECT type_id INTO v_type_id
      FROM carte_membre
     WHERE client_id = p_client AND etat = 1;

    -- Get how many books allowed
    SELECT nbr_livre_autorise INTO v_allowed
      FROM member_type
     WHERE id = v_type_id;

    -- Get current number of unreturned loans
    SELECT COUNT(*) INTO v_current
      FROM location_livre
     WHERE client_id = p_client
       AND date_retour IS NULL;

    IF v_current < v_allowed THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0; -- no valid membership
END can_borrow;


-------------------------------------------------
-- PROCEDURE: rent a book
-------------------------------------------------
PROCEDURE rent_book(
    p_client IN NUMBER,
    p_livre IN NUMBER
)
IS
    v_allowed NUMBER;
    v_stock NUMBER;
BEGIN
    -- 1. Check membership
    v_allowed := can_borrow(p_client);
    IF v_allowed = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Client cannot borrow more books or has no valid membership');
    END IF;

    -- 2. Check stock
    SELECT stock INTO v_stock FROM livres WHERE id = p_livre;
    IF v_stock <= 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'This book is currently out of stock');
    END IF;

    -- 3. Insert borrowing record
    INSERT INTO location_livre (livre_id, client_id, date_sortie)
    VALUES (p_livre, p_client, SYSDATE);

    -- 4. Deduct stock
    UPDATE livres SET stock = stock - 1 WHERE id = p_livre;

END rent_book;


-------------------------------------------------
-- PROCEDURE: return a book
-------------------------------------------------
PROCEDURE return_book(
    p_location_id IN NUMBER
)
IS
    v_livre NUMBER;
BEGIN
    -- Get book ID
    SELECT livre_id INTO v_livre
    FROM location_livre
    WHERE id = p_location_id;

    -- Update return date
    UPDATE location_livre
    SET date_retour = SYSDATE
    WHERE id = p_location_id;

    -- Restore stock
    UPDATE livres
    SET stock = stock + 1
    WHERE id = v_livre;

END return_book;

END library_api;
