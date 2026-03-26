SELECT
    c.client_id,
    c.last_name,
    c.first_name,
    c.city,
    COUNT(o.order_id) AS orders_count,
    ROUND(SUM(f.price * (100 - o.discount_percent) / 100), 2) AS total_spent,
    ROUND(AVG(o.discount_percent), 1) AS avg_discount_received,
    RANK() OVER (ORDER BY SUM(f.price * (100 - o.discount_percent) / 100) DESC) AS spending_rank,
    RANK() OVER (ORDER BY COUNT(o.order_id) DESC) AS frequency_rank,
    RANK() OVER (ORDER BY AVG(o.discount_percent) DESC) AS discount_rank,
    ROUND(
            (RANK() OVER (ORDER BY SUM(f.price * (100 - o.discount_percent) / 100) DESC) * 0.5 +
             RANK() OVER (ORDER BY COUNT(o.order_id) DESC) * 0.3 +
             RANK() OVER (ORDER BY AVG(o.discount_percent) DESC) * 0.2)
        , 1) AS loyalty_score,
    CASE
        WHEN (RANK() OVER (ORDER BY SUM(f.price * (100 - o.discount_percent) / 100) DESC) * 0.5 +
              RANK() OVER (ORDER BY COUNT(o.order_id) DESC) * 0.3 +
              RANK() OVER (ORDER BY AVG(o.discount_percent) DESC) * 0.2) <= 5 THEN 'VIP'
        WHEN (RANK() OVER (ORDER BY SUM(f.price * (100 - o.discount_percent) / 100) DESC) * 0.5 +
              RANK() OVER (ORDER BY COUNT(o.order_id) DESC) * 0.3 +
              RANK() OVER (ORDER BY AVG(o.discount_percent) DESC) * 0.2) <= 10 THEN 'Постоянный'
        ELSE 'Обычный'
        END AS loyalty_tier
FROM clients c
         JOIN orders o ON c.client_id = o.client_id
         JOIN furniture f ON o.product_code = f.product_code
GROUP BY c.client_id
ORDER BY loyalty_score;