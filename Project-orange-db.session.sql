
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

TRUNCATE TABLE warehouse_productorder RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_packing RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_order RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_production RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_product RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_group RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_branch RESTART IDENTITY CASCADE;

INSERT INTO warehouse_group ("group")
VALUES
    ('#1'),
    ('#2'),
    ('#3'),
    ('#4'),
    ('#5'),
    ('#6'),
    ('#7');

INSERT INTO warehouse_product ("name", "group_id")
VALUES
    ('Friterad Orange Chicken', 3),
    ('WOKBIFF', 2),
    ('Spicy Lime Chicken', 4),
    ('Friterad Spicy Lime Chicken', 4),
    ('Orange Chicken', 3),
    ('Peanut Chicken', 1),
    ('Wokkyckling', 7);

INSERT INTO warehouse_production (batch, lot, product_id)
VALUES
    ('PROD0000000004', '1006', 2),
    ('PROD0000000002', '1003', 6),
    ('PROD0000000006', '1001', 1),
    ('PROD0000000001', '1005', 4),
    ('PROD0000000005', '1002', 3),
    ('PROD0000000003', '1004', 5),
    ('PROD0000000007', '1007', 7);

INSERT INTO warehouse_packing (
    quantity,
    packing_date,
    best_before,
    production_id,
    product_id
)
VALUES
    (1500, current_date, current_date + interval '1 year', 2, 4),
    (500, current_date, current_date + interval '1 year', 4, 1),
    (2000, current_date, current_date + interval '1 year', 1, 3),
    (1000, current_date, current_date + interval '1 year', 3, 2);

SELECT * FROM warehouse_group;
SELECT * FROM warehouse_product;
SELECT * FROM warehouse_production;
SELECT * FROM warehouse_packing;

SELECT
    wpk.packing_id,
    wpk.production_id,
    wp.name,
    wp.product_id,
    wpk.packing_date,
    wpk.best_before,
    wpk.quantity
FROM warehouse_packing AS wpk
INNER JOIN warehouse_product AS wp ON wpk.product_id = wp.product_id;