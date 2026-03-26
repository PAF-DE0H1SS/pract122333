SELECT
    c.client_id,
    c.last_name,
    c.first_name,
    c.middle_name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(f.price * (100 - o.discount_percent) / 100), 2) AS total_spent,
    ROUND(AVG(o.discount_percent), 1) AS avg_discount
FROM clients c
         JOIN orders o ON c.client_id = o.client_id
         JOIN furniture f ON o.product_code = f.product_code
GROUP BY c.client_id
HAVING total_spent > 100000
ORDER BY total_spent DESC;