INSERT INTO warehouse_restaurant (city, district)
VALUES ('Arninge', NULL),
    ('Borlänge', NULL),
    ('Borås', NULL),
    ('Bromma', NULL),
    ('Enköping', NULL),
    ('Eskilstuna', NULL),
    ('Falun', NULL),
    ('Farsta', NULL),
    ('Gävle', NULL),
    ('Häggvik', NULL),
    ('Jönköping', NULL),
    ('Kalmar', NULL),
    ('Karlstad', NULL),
    ('Kristianstad', NULL),
    ('Kungsbacka', NULL),
    ('Linköping', NULL),
    ('Lund', NULL),
    ('Malmö', 'Lockarp'),
    ('Malmö', 'Svågertorp'),
    ('Mjölby', NULL),
    ('Motala', NULL),
    ('Märsta', NULL),
    ('Norrtälje', NULL),
    ('Nyköping', NULL),
    ('Haninge', 'Port 73'),
    ('Rosersberg', NULL),
    ('Rotebro', NULL),
    ('Sickla', NULL),
    ('Strängnäs', NULL),
    ('Sundsvall', NULL),
    ('Trollhättan', NULL),
    ('Uddevalla', NULL),
    ('Umeå', 'Ersboda'),
    ('Uppsala', 'Boländerna'),
    ('Uppsala', 'Gränby'),
    ('Varberg', NULL),
    ('Värmdö', NULL),
    ('Värnamo', NULL),
    ('Västerås', 'Erikslund'),
    ('Västerås', 'Gryta'),
    ('Växjö', NULL),
    ('Örebro', 'Eurostop'),
    ('Örebro', 'Krämaren') ON CONFLICT ("restaurant_id") DO NOTHING;


INSERT INTO warehouse_group ("group")
VALUES ('#1'),
    ('#2'),
    ('#3'),
    ('#4'),
    ('#5'),
    ('#6'),
    ('#7'),
    ('#8'),
    ('#9'),
    ('#10') ON CONFLICT ("group_id") DO NOTHING;

INSERT INTO warehouse_product ("name", "group_id")
VALUES ('Orange Chicken', 3),
    ('Friterad Orange Chicken', 3),
    ('Spicy Lime Chicken', 4),
    ('Friterad Spicy Lime Chicken', 4),
    ('Peanut Chicken', 1),
    ('Peanut Chicken sås', 1),
    ('WOKBIFF', 2),
    ('Wokkyckling', 7) ON CONFLICT ("product_id") DO NOTHING;

INSERT INTO warehouse_production (batch, lot, volume, product_id)
VALUES (
        'PROD0000000366',
        '76497',
        5000,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'WOKBIFF'
        )
    ),
    (
        'PROD0000000410',
        'V923471',
        3000,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Wokkyckling'
        )
    ),
    (
        'PROD0000000325',
        'V923471/v923484',
        12600,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Spicy Lime Chicken'
        )
    ),
    (
        'PROD0000000320',
        'V923471/v923484',
        6000,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Spicy Lime Chicken'
        )
    ),
    (
        'PROD0000000315',
        'v923484',
        12000,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Orange Chicken'
        )
    ),
    (
        'PROD0000000310',
        'v923484',
        6000,
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Orange Chicken'
        )
    )
    ON CONFLICT ("production_id") DO NOTHING;

INSERT INTO warehouse_packing (
        production_id,
        product_id,
        packing_date,
        best_before,
        quantity
    )
VALUES (
        (
            SELECT production_id
            FROM warehouse_production
            WHERE batch = 'PROD0000000315'
        ),
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Orange Chicken'
        ),
        '2025-06-13',
        '2026-06-13',
        2800
    ),
    (
        (
            SELECT production_id
            FROM warehouse_production
            WHERE batch = 'PROD0000000325'
        ),
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Spicy Lime Chicken'
        ),
        '2025-06-13',
        '2026-06-13',
        2200
    ),
    (
        (
            SELECT production_id
            FROM warehouse_production
            WHERE batch = 'PROD0000000366'
        ),
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'WOKBIFF'
        ),
        '2025-06-09',
        '2026-06-09',
        380
    ),
    (
        (
            SELECT production_id
            FROM warehouse_production
            WHERE batch = 'PROD0000000410'
        ),
        (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Wokkyckling'
        ),
        '2025-06-11',
        '2026-06-11',
        2200
    ) ON CONFLICT ("packing_id") DO NOTHING;
INSERT INTO warehouse_order (restaurant_id, created_at, "status")
VALUES (
        (
            SELECT restaurant_id
            FROM warehouse_restaurant
            WHERE "name" = 'Rosersberg'
        ),
        '2025-08-20 09:20:07',
        'PROCESSING'
    ),
    (
        (
            SELECT restaurant_id
            FROM warehouse_restaurant
            WHERE "name" = 'Port 73 Haninge'
        ),
        '2025-08-20 10:00:59',
        'CREATED'
    ),
    (
        (
            SELECT restaurant_id
            FROM warehouse_restaurant
            WHERE "name" = 'Port 73 Haninge'
        ),
        '2025-08-20 10:00:59',
        'PROCESSING'
    ),
    (
        (
            SELECT restaurant_id
            FROM warehouse_restaurant
            WHERE "name" = 'Farsta'
        ),
        '2025-08-20 12:15:05',
        'COMPLETED'
    ) ON CONFLICT ("order_id") DO NOTHING;
INSERT INTO warehouse_productorder (order_id, product_id, quantity)
VALUES (
        (
            SELECT order_id
            FROM warehouse_order
            WHERE restaurant_id = (
                    SELECT restaurant_id
                    FROM warehouse_restaurant
                    WHERE "name" = 'Rosersberg'
                )
            ORDER BY created_at DESC
            LIMIT 1
        ), (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'WOKBIFF'
        ),
        10
    ),
    (
        (
            SELECT order_id
            FROM warehouse_order
            WHERE restaurant_id = (
                    SELECT restaurant_id
                    FROM warehouse_restaurant
                    WHERE "name" = 'Port 73 Haninge'
                )
            ORDER BY created_at DESC
            LIMIT 1
        ), (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Wokkyckling'
        ),
        40
    ),
    (
        (
            SELECT order_id
            FROM warehouse_order
            WHERE restaurant_id = (
                    SELECT restaurant_id
                    FROM warehouse_restaurant
                    WHERE "name" = 'Port 73 Haninge'
                )
            ORDER BY created_at ASC
            LIMIT 1
        ), (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Orange Chicken'
        ),
        20
    ),
    (
        (
            SELECT order_id
            FROM warehouse_order
            WHERE restaurant_id = (
                    SELECT restaurant_id
                    FROM warehouse_restaurant
                    WHERE "name" = 'Farsta'
                )
            ORDER BY created_at DESC
            LIMIT 1
        ), (
            SELECT product_id
            FROM warehouse_product
            WHERE "name" = 'Friterad Orange Chicken'
        ),
        20
    );
SELECT *
FROM warehouse_group;
SELECT *
FROM warehouse_restaurant;
SELECT *
FROM warehouse_product;
SELECT *
FROM warehouse_production;
SELECT *
FROM warehouse_packing;
SELECT *
FROM warehouse_order;
SELECT *
FROM warehouse_productorder;

SELECT wpk.packing_id,
    wpk.production_id,
    wp.name,
    wp.product_id,
    wpk.packing_date,
    wpk.best_before,
    wpk.quantity
FROM warehouse_packing AS wpk
    INNER JOIN warehouse_product AS wp ON wpk.product_id = wp.product_id;

DELETE FROM warehouse_production
WHERE lot = 'V923471'