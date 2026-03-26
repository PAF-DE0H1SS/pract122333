SELECT
    o.order_id,
    c.last_name || ' ' || c.first_name AS client_name,
    f.name AS furniture_name,
    f.type,
    f.price AS original_price,
    o.discount_percent,
    ROUND(f.price * (100 - o.discount_percent) / 100, 2) AS final_price,
    type_avg.avg_price_by_type,
    ROUND(ABS((f.price * (100 - o.discount_percent) / 100 - type_avg.avg_price_by_type) / type_avg.avg_price_by_type * 100), 1) AS deviation_percent,
    CASE
        WHEN (f.price * (100 - o.discount_percent) / 100) > type_avg.avg_price_by_type * 1.3 THEN 'Выше нормы'
        WHEN (f.price * (100 - o.discount_percent) / 100) < type_avg.avg_price_by_type * 0.7 THEN 'Ниже нормы'
        END AS anomaly_type
FROM orders o
         JOIN clients c ON o.client_id = c.client_id
         JOIN furniture f ON o.product_code = f.product_code
         JOIN (
    SELECT
        f2.type,
        AVG(f2.price * (100 - o2.discount_percent) / 100) AS avg_price_by_type
    FROM furniture f2
             JOIN orders o2 ON f2.product_code = o2.product_code
    GROUP BY f2.type
) type_avg ON f.type = type_avg.type
WHERE (f.price * (100 - o.discount_percent) / 100) > type_avg.avg_price_by_type * 1.3
   OR (f.price * (100 - o.discount_percent) / 100) < type_avg.avg_price_by_type * 0.7
ORDER BY deviation_percent DESC;