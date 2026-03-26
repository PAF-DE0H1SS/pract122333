WITH discount_ranges AS (
    SELECT
        CASE
            WHEN o.discount_percent = 0 THEN '0% (без скидки)'
            WHEN o.discount_percent BETWEEN 1 AND 10 THEN '1-10%'
            WHEN o.discount_percent BETWEEN 11 AND 20 THEN '11-20%'
            ELSE '20%+'
            END AS discount_group,
        o.order_id,
        f.price,
        o.discount_percent,
        f.items_count
    FROM orders o
             JOIN furniture f ON o.product_code = f.product_code
)
SELECT
    discount_group,
    COUNT(order_id) AS orders_count,
    ROUND(AVG(discount_percent), 1) AS avg_discount,
    ROUND(AVG(price), 2) AS avg_original_price,
    ROUND(AVG(price * (100 - discount_percent) / 100), 2) AS avg_final_price,
    SUM(items_count) AS total_items_sold,
    ROUND(AVG(items_count), 1) AS avg_items_per_order
FROM discount_ranges
GROUP BY discount_group
ORDER BY
    CASE discount_group
        WHEN '0% (без скидки)' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        ELSE 4
        END;