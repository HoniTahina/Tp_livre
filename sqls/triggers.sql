CREATE OR REPLACE TRIGGER check_stock_before_rent
BEFORE INSERT ON location_livre
FOR EACH ROW
DECLARE
    v_stock NUMBER;
BEGIN
    SELECT stock INTO v_stock FROM livres WHERE id = :NEW.livre_id;
    IF v_stock <= 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Impossible : livre en rupture de stock');
    END IF;
END;