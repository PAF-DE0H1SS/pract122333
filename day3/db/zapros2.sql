SELECT
    o.order_id,
    c.client_id,
    c.last_name,
    c.first_name,
    c.middle_name,
    c.city,
    f.product_code,
    f.name AS furniture_name,
    f.type AS furniture_type,
    f.country,
    o.order_date,
    o.discount_percent,
    ROUND(f.price * (100 - o.discount_percent) / 100, 2) AS final_price
FROM orders o
         INNER JOIN clients c ON o.client_id = c.client_id
         INNER JOIN furniture f ON o.product_code = f.product_code
WHERE c.last_name LIKE 'Д%'
   OR c.last_name LIKE 'Р%'
ORDER BY c.last_name, o.order_date;