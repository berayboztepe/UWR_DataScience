BEGIN;

-- Zadanie 1

CREATE MATERIALIZED VIEW skill_offer_mat_view AS
SELECT name AS skill, city,
    SUM((type = 'permanent')::integer) AS permanent_offers,
    SUM((type = 'b2b')::integer) AS b2b_offers
  FROM skill NATURAL JOIN employment_details
    JOIN offer ON offer_id = id 
  GROUP BY city, name 
  HAVING SUM((type = 'permanent')::integer)>0 OR SUM((type = 'b2b')::integer) >0 ;


REFRESH MATERIALIZED VIEW skill_offer_mat_view;

-- Zadanie 2

CREATE TABLE skill_offer_table (
  skill TEXT, city TEXT, permanent_offers INT, b2b_offers INT,
  PRIMARY KEY (skill, city)
);

INSERT INTO skill_offer_table
  SELECT s.name AS skill, o.city,
    SUM((ed.type = 'permanent')::integer) AS permanent_offers,
    SUM((ed.type = 'b2b')::integer) AS b2b_offers
  FROM skill s NATURAL JOIN 
       employment_details ed JOIN
       offer o ON offer_id = id
  GROUP BY o.city, s.name
  HAVING SUM((type = 'permanent')::integer)>0 OR SUM((type = 'b2b')::integer) >0;

-- Zadanie 3

-- INSERT

CREATE OR REPLACE FUNCTION ins() RETURNS TRIGGER AS $O$
DECLARE
  thiscity TEXT;
  is_perm BOOL;
  is_b2b BOOL;
BEGIN
  SELECT city,
      BOOL_OR(type = 'permanent'),
      BOOL_OR(type = 'b2b')
    INTO thiscity, is_perm, is_b2b
    FROM offer JOIN employment_details ON id = offer_id
    WHERE id = NEW.offer_id
    GROUP BY city;
  IF NOT (is_perm OR is_b2b) THEN
    RETURN NEW;
  END IF;
  IF (NEW.name, thiscity) IN (
    SELECT skill, city FROM skill_offer_table
  ) THEN
    UPDATE skill_offer_table
      SET permanent_offers = permanent_offers + is_perm::INT,
        b2b_offers = b2b_offers + is_b2b::INT
      WHERE skill = NEW.name AND city = thiscity;
  ELSE
    INSERT INTO skill_offer_table VALUES
      (NEW.name, thiscity, is_perm::INT, is_b2b::INT);
  END IF;
  RETURN NEW;
END;
$O$ LANGUAGE plpgsql;

CREATE TRIGGER ins AFTER INSERT ON skill
FOR EACH ROW EXECUTE PROCEDURE ins();

-- DELETE

CREATE OR REPLACE FUNCTION del() RETURNS TRIGGER AS $O$
DECLARE
  thiscity TEXT;
  is_perm BOOL;
  is_b2b BOOL;
BEGIN
  SELECT city,
      BOOL_OR(type = 'permanent'),
      BOOL_OR(type = 'b2b')
    INTO thiscity, is_perm, is_b2b
    FROM offer JOIN employment_details ON id = offer_id
    WHERE id = OLD.offer_id
    GROUP BY city;
  IF NOT (is_perm OR is_b2b) THEN
    RETURN OLD;
  END IF;
  IF (is_perm::INT, is_b2b::INT) = (
    SELECT permanent_offers, b2b_offers
      FROM skill_offer_table
      WHERE skill = OLD.name AND city = thiscity
  ) THEN
    DELETE FROM skill_offer_table
      WHERE skill = OLD.name AND city = thiscity;
  ELSE
    UPDATE skill_offer_table
      SET permanent_offers = permanent_offers - is_perm::INT,
        b2b_offers = b2b_offers - is_b2b::INT
      WHERE skill = OLD.name AND city = thiscity;
  END IF;
  RETURN OLD;
END;
$O$ LANGUAGE plpgsql;

CREATE TRIGGER del AFTER DELETE ON skill
FOR EACH ROW EXECUTE PROCEDURE del();

-- UPDATE
-- zmianę name gwarantuje klauzula WHEN w CREATE TRIGGER
-- brak zmiany offer_id (a więc i miasta) gwarantuje treść zadania

CREATE OR REPLACE FUNCTION upd() RETURNS TRIGGER AS $O$
DECLARE
  thiscity TEXT;
  is_perm BOOL;
  is_b2b BOOL;
BEGIN
  SELECT city,
      BOOL_OR(type = 'permanent'),
      BOOL_OR(type = 'b2b')
    INTO thiscity, is_perm, is_b2b
    FROM offer JOIN employment_details ON id = offer_id
    WHERE id = OLD.offer_id
    GROUP BY city;
  IF NOT (is_perm OR is_b2b) THEN
    RETURN NEW;
  END IF;
  -- poniższy IF-ELSE skopiowany z ins()
  IF (NEW.name, thiscity) IN (
    SELECT skill, city FROM skill_offer_table
  ) THEN
    UPDATE skill_offer_table
      SET permanent_offers = permanent_offers + is_perm::INT,
        b2b_offers = b2b_offers + is_b2b::INT
      WHERE skill = NEW.name AND city = thiscity;
  ELSE
    INSERT INTO skill_offer_table VALUES
      (NEW.name, thiscity, is_perm::INT, is_b2b::INT);
  END IF;
  -- poniższy IF-ELSE skopiowany z del()
  IF (is_perm::INT, is_b2b::INT) = (
    SELECT permanent_offers, b2b_offers
      FROM skill_offer_table
      WHERE skill = OLD.name AND city = thiscity
  ) THEN
    DELETE FROM skill_offer_table
      WHERE skill = OLD.name AND city = thiscity;
  ELSE
    UPDATE skill_offer_table
      SET permanent_offers = permanent_offers - is_perm::INT,
        b2b_offers = b2b_offers - is_b2b::INT
      WHERE skill = OLD.name AND city = thiscity;
  END IF; 
  RETURN NEW;
END;
$O$ LANGUAGE plpgsql;

CREATE TRIGGER upd AFTER UPDATE ON skill
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FROM NEW.name)
EXECUTE PROCEDURE upd();

-- testy

SELECT * FROM skill_offer_table
  WHERE city = 'Żyrardów' AND skill LIKE 'C%';

INSERT INTO skill VALUES ('C++', 31337, 3901), ('Caml', 161, 4774);

SELECT * FROM skill_offer_table
  WHERE city = 'Żyrardów' AND skill LIKE 'C%';

DELETE FROM skill
  WHERE (name, offer_id) = ('C++', 3901)
    OR (name, offer_id) = ('Caml', 4774);

SELECT * FROM skill_offer_table
  WHERE city = 'Żyrardów' AND skill LIKE 'C%';

UPDATE skill SET name = 'Caml'
  WHERE (name, offer_id) = ('C++', '4774');
UPDATE skill SET name = 'C#'
  WHERE (name, offer_id) = ('C', 9522);

SELECT * FROM skill_offer_table
  WHERE city = 'Żyrardów' AND skill LIKE 'C%';

ROLLBACK;
