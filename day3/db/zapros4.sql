SELECT
    o.order_id,
    c.last_name || ' ' || c.first_name AS client_name,
    f.name AS furniture_name,
    f.price AS original_price,
    o.discount_percent,
    ROUND(f.price * (100 - o.discount_percent) / 100, 2) AS final_price,
    o.order_date
FROM orders o
         JOIN clients c ON o.client_id = c.client_id
         JOIN furniture f ON o.product_code = f.product_code
ORDER BY final_price DESC
LIMIT 5;