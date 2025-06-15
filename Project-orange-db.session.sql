TRUNCATE TABLE warehouse_productorder RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_packing RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_order RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_production RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_product RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_group RESTART IDENTITY CASCADE;
TRUNCATE TABLE warehouse_branch RESTART IDENTITY CASCADE;

INSERT INTO warehouse_group ("group")
VALUES ('#1'),
    ('#2'),
    ('#3'),
    ('#4'),
    ('#5'),
    ('#6'),
    ('#7');

INSERT INTO warehouse_product ("name", "group_id")
VALUES ('Peanut Chicken', 1),
    ('WOKBIFF', 2),
    ('Orange Chicken', 3),
    ('Friterad Orange Chicken', 3),
    ('Spicy Lime Chicken', 4),
    ('Friterad Spicy Lime Chicken', 4);

INSERT INTO warehouse_production (batch, lot, "date", product_id)
VALUES ('PROD0000000001', '0001', current_date - interval '1 day', 1),
    ('PROD0000000002', '0002', current_date - interval '2 day', 2),
    ('PROD0000000003', '0003', current_date - interval '3 day', 3),
    ('PROD0000000004', '0004', current_date - interval '4 day', 4),
    ('PROD0000000005', '0005', current_date - interval '5 day', 5),
    ('PROD0000000006', '0006', current_date - interval '6 day', 6);

INSERT INTO warehouse_packing (
        quantity,
        "date",
        best_before,
        production_id,
        product_id
    )
VALUES (
        500,
        current_date,
        current_date + interval '1 year',
        3,
        3
    );

SELECT *
FROM warehouse_group;
SELECT *
FROM warehouse_product;
SELECT *
FROM warehouse_production;
SELECT *
FROM warehouse_packing;

SELECT *
FROM warehouse_product AS wp
JOIN warehouse_packing AS wpk ON wp.product_id = wpk.product_id
WHERE wp.product_id = 3;