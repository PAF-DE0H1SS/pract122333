SELECT
    c.client_id,
    c.last_name,
    c.first_name,
    c.middle_name,
    c.city,
    COUNT(o.order_id) AS orders_count,
    GROUP_CONCAT(f.name, '; ') AS purchased_items
FROM clients c
         JOIN orders o ON c.client_id = o.client_id
         JOIN furniture f ON o.product_code = f.product_code
WHERE c.client_id NOT IN (
    SELECT DISTINCT client_id
    FROM orders
    WHERE discount_percent > 0
)
GROUP BY c.client_id;