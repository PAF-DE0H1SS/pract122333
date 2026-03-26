SELECT
    c.client_id,
    c.last_name,
    c.first_name,
    c.middle_name,
    f.name AS furniture_name,
    f.product_code,
    f.country,
    o.order_date,
    o.discount_percent,
    ROUND(f.price * (100 - o.discount_percent) / 100, 2) AS final_price
FROM orders o
         INNER JOIN clients c ON o.client_id = c.client_id
         INNER JOIN furniture f ON o.product_code = f.product_code
WHERE f.type = 'кухонная'
  AND f.country = 'Россия'
  AND o.discount_percent >= 10
ORDER BY o.discount_percent DESC, c.last_name;