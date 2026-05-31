-- 1. Топ-5 подкатегорий с накопительной прибылью (ABC-анализ)
SELECT 
    sub_category,
    SUM(profit) as total_profit,
    ROUND(100.0 * SUM(profit) / SUM(SUM(profit)) OVER (), 2) as profit_share,
    SUM(SUM(profit)) OVER (ORDER BY SUM(profit) DESC) as cumulative_profit
FROM superstore_sales
GROUP BY sub_category
ORDER BY total_profit DESC
LIMIT 5;

-- 2. Сравнение прибыли клиента со следующим (анализ отрывов)
SELECT 
    customer_name,
    SUM(profit) as profit,
    LEAD(SUM(profit)) OVER (ORDER BY SUM(profit) DESC) as next_profit,
    SUM(profit) - LEAD(SUM(profit)) OVER (ORDER BY SUM(profit) DESC) as gap
FROM superstore_sales
GROUP BY customer_name
ORDER BY profit DESC
LIMIT 10;

-- 3. Ежемесячная прибыль с накоплением (YTD)
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(profit) as monthly_profit,
    SUM(SUM(profit)) OVER (ORDER BY DATE_TRUNC('month', order_date)) as ytd_profit
FROM superstore_sales
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;