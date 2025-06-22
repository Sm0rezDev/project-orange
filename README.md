# project-orange

Description:
A simple Warehouse & Production backend serving API endpoints.

# Goal:
- get a simple backend application running with backend framework "Django".
- build a containerized docker image.
- Push built image to a registry
- Docker compose to pull and setup the container image with database environment up.


# API Endpoints

```
http://{{host}}/wp/status/


// Inventory status
{
    "table": "products",
    "max_rows": 10,
    "fields": [
        // "product_id",
        // "production_id",
        // "packing_date",
        // "best_before",
        // "quantity",
        // "product__name"
    ]
}

// Active Production's
{
    "table": "productions",
    "max_rows": 10,
    "fields": [
    ]
}

// Order status
{
    "table": "orders",
    "max_rows": 10,
    
    "fields": [
        "order_id",
        "product__name",
        "order__status",
        "order__created_at",
        "order__restaurant__city",
        "order__restaurant__district",
        "quantity"
    ]
}
```

```
http://{{host}}/wp/production/new/

// Add production
{
    "product_id": "friterad orange chicken",
    "batch": "PROD0000000100",
    "lot": "V923471",
    "volume": 9000
}

```
http://{{host}}/wp/packing/
// Add packing
{
    "production_id": 4,
    "product_id": 1,
    "quantity": 1
}
```

```
http://localhost:8000/wp/order/new/
// Add order
{
    //"restaurant_id": 25,
    //"city": "haninge",
    "district": "port 73",
    "products": [
        { "product": "WOKBIFF", "quantity": 10 },
        { "product": "spicy lime chicken", "quantity": 36 }
    ]
}
```