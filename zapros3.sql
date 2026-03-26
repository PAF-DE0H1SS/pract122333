SELECT
    f.country,
    COUNT(DISTINCT o.order_id) AS orders_count,
    SUM(f.items_count) AS total_items_sold,
    ROUND(SUM(f.price * (100 - o.discount_percent) / 100), 2) AS total_revenue,
    ROUND(AVG(o.discount_percent), 1) AS avg_discount_percent,
    ROUND(SUM(f.price * (100 - o.discount_percent) / 100) / COUNT(o.order_id), 2) AS avg_order_value
FROM orders o
         JOIN furniture f ON o.product_code = f.product_code
GROUP BY f.country
ORDER BY total_revenue DESC;