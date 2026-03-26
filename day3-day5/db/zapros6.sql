SELECT
    strftime('%Y-%m', o.order_date) AS month,
    f.type,
    COUNT(o.order_id) AS orders_count,
    ROUND(SUM(f.price * (100 - o.discount_percent) / 100), 2) AS monthly_revenue,
    ROUND(AVG(o.discount_percent), 1) AS avg_discount,
    ROUND(SUM(SUM(f.price * (100 - o.discount_percent) / 100)) OVER (
        PARTITION BY f.type ORDER BY strftime('%Y-%m', o.order_date)
        ), 2) AS cumulative_revenue
FROM orders o
         JOIN furniture f ON o.product_code = f.product_code
GROUP BY month, f.type
ORDER BY month, f.type;