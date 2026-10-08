-- IT Support Ticket Analysis: Business SQL
-- Dialect: SQLite 3.x
-- Load: CREATE TABLE tickets AS SELECT * FROM read_csv_auto(...) for DuckDB,
-- or import synthetic_it_support_tickets.csv into a table named tickets.

-- 1. Overall KPI
SELECT
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(100.0 * AVG(CASE WHEN status = 'resolved' THEN 1.0 ELSE 0 END), 2) AS resolved_rate_pct,
    ROUND(100.0 * AVG(CASE WHEN status IN ('open','in_progress','on_hold') THEN 1.0 ELSE 0 END), 2) AS backlog_rate_pct,
    ROUND(100.0 * AVG(reopened), 2) AS reopen_rate_pct,
    ROUND(AVG(csat_score), 2) AS avg_csat,
    ROUND(100.0 * AVG(CASE WHEN customer_sentiment IN ('negative','very_negative') THEN 1.0 ELSE 0 END), 2) AS negative_sentiment_pct,
    ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hours
FROM tickets;

-- 2. Status / backlog
SELECT status, COUNT(*) AS tickets,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_tickets
FROM tickets
GROUP BY status
ORDER BY tickets DESC;

-- 3. Monthly ticket trend
SELECT substr(created_at,1,7) AS year_month,
       COUNT(*) AS tickets,
       ROUND(100.0 * AVG(CASE WHEN status='resolved' THEN 1.0 ELSE 0 END),2) AS resolved_rate_pct,
       ROUND(AVG(csat_score),2) AS avg_csat
FROM tickets
GROUP BY substr(created_at,1,7)
ORDER BY year_month;

-- 4. Issue type performance
SELECT issue_type,
       COUNT(*) AS tickets,
       ROUND(100.0 * AVG(CASE WHEN status='resolved' THEN 1.0 ELSE 0 END),2) AS resolved_rate_pct,
       ROUND(AVG(resolution_time_hours),2) AS avg_resolution_hours,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(100.0 * AVG(CASE WHEN customer_sentiment IN ('negative','very_negative') THEN 1.0 ELSE 0 END),2) AS negative_sentiment_pct,
       ROUND(100.0 * AVG(reopened),2) AS reopen_rate_pct
FROM tickets
GROUP BY issue_type
ORDER BY avg_csat ASC;

-- 5. Product area performance
SELECT product_area,
       COUNT(*) AS tickets,
       ROUND(100.0 * AVG(CASE WHEN status='resolved' THEN 1.0 ELSE 0 END),2) AS resolved_rate_pct,
       ROUND(AVG(resolution_time_hours),2) AS avg_resolution_hours,
       ROUND(AVG(csat_score),2) AS avg_csat
FROM tickets
GROUP BY product_area
ORDER BY tickets DESC;

-- 6. Priority effectiveness
SELECT priority,
       COUNT(*) AS tickets,
       ROUND(AVG(resolution_time_hours),2) AS avg_resolution_hours,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(100.0 * AVG(reopened),2) AS reopen_rate_pct,
       ROUND(100.0 * AVG(CASE WHEN status IN ('open','in_progress','on_hold') THEN 1.0 ELSE 0 END),2) AS backlog_rate_pct
FROM tickets
GROUP BY priority
ORDER BY CASE priority
           WHEN 'urgent' THEN 1 WHEN 'high' THEN 2
           WHEN 'medium' THEN 3 WHEN 'low' THEN 4 ELSE 5 END;

-- 7. Channel comparison
SELECT channel,
       COUNT(*) AS tickets,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(AVG(resolution_time_hours),2) AS avg_resolution_hours,
       ROUND(100.0 * AVG(reopened),2) AS reopen_rate_pct
FROM tickets
GROUP BY channel
ORDER BY avg_csat DESC;

-- 8. Customer segment
SELECT customer_segment,
       COUNT(*) AS tickets,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(100.0 * AVG(CASE WHEN customer_sentiment IN ('negative','very_negative') THEN 1.0 ELSE 0 END),2) AS negative_sentiment_pct,
       ROUND(AVG(resolution_time_hours),2) AS avg_resolution_hours
FROM tickets
GROUP BY customer_segment
ORDER BY avg_csat DESC;

-- 9. SLA plan comparison
SELECT sla_plan,
       COUNT(*) AS tickets,
       ROUND(100.0 * AVG(CASE WHEN status='resolved' THEN 1.0 ELSE 0 END),2) AS resolved_rate_pct,
       ROUND(100.0 * AVG(CASE WHEN status IN ('open','in_progress','on_hold') THEN 1.0 ELSE 0 END),2) AS backlog_rate_pct,
       ROUND(AVG(csat_score),2) AS avg_csat
FROM tickets
GROUP BY sla_plan
ORDER BY CASE sla_plan WHEN 'platinum' THEN 1 WHEN 'gold' THEN 2 WHEN 'standard' THEN 3 ELSE 4 END;

-- 10. Region data quality + KPIs
SELECT COALESCE(region,'Unknown') AS region,
       COUNT(*) AS tickets,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(100.0 * AVG(CASE WHEN status IN ('open','in_progress','on_hold') THEN 1.0 ELSE 0 END),2) AS backlog_rate_pct
FROM tickets
GROUP BY COALESCE(region,'Unknown')
ORDER BY tickets DESC;

-- 11. Customer-level workload / concentration
SELECT customer_id,
       COUNT(*) AS ticket_count,
       ROUND(AVG(csat_score),2) AS avg_csat,
       ROUND(100.0 * AVG(reopened),2) AS reopen_rate_pct
FROM tickets
GROUP BY customer_id
ORDER BY ticket_count DESC
LIMIT 20;

-- 12. High-risk operational queue:
-- unresolved + high/urgent priority + negative sentiment
SELECT priority, issue_type, product_area,
       COUNT(*) AS high_risk_tickets,
       ROUND(AVG(csat_score),2) AS avg_csat
FROM tickets
WHERE status IN ('open','in_progress','on_hold')
  AND priority IN ('high','urgent')
  AND customer_sentiment IN ('negative','very_negative')
GROUP BY priority, issue_type, product_area
ORDER BY high_risk_tickets DESC;
