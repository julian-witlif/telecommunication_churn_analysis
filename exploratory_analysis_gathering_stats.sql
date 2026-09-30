select * from sandbox.public.customer_churn;

--Spalten mit gleichen werten: Count, Country, State

--Dont include logistic regression: City (to few values for relevance), geo location

--To consider monthly charges should be treated as continues value in logistic regression

--multiple lines: No, No phone service, Yes

--internet_service: DSL, Fiber optic, No

select * from sandbox.public.customer_churn
where total_charges is null or monthly_charges is null;

select distinct payment_method from sandbox.public.customer_churn;
--Credit card (automatic)
--Bank transfer (automatic)
--Mailed check
--Electronic check

select distinct phone_service from sandbox.public.customer_churn;


SELECT 
    contract,
    AVG(CASE WHEN churn_label = 'Yes' THEN 1.0 ELSE 0.0 END)*100 AS Churn_Rate,
    COUNT(*) AS Count
FROM sandbox.public.customer_churn
GROUP BY contract
ORDER BY Churn_Rate DESC;


SELECT 
    dependents,
    round(AVG(CASE WHEN churn_label = 'Yes' THEN 1.0 ELSE 0.0 END), 4) AS churn_rate,
    COUNT(*) AS Count
FROM sandbox.public.customer_churn
GROUP BY dependents
ORDER BY Churn_Rate DESC;
--DEPENDENTS	CHURN_RATE	COUNT
--FALSE	0.3255	5416
--TRUE	0.0652	1627

select dependents, churn_label, count(*)
from sandbox.public.customer_churn
group by dependents, churn_label;


with cte as(
SELECT 
    CASE 
        WHEN tenure_months BETWEEN 0 AND 12 THEN '0-12'
        WHEN tenure_months BETWEEN 13 AND 24 THEN '13-24'
        WHEN tenure_months BETWEEN 25 AND 36 THEN '25-36'
        WHEN tenure_months BETWEEN 37 AND 48 THEN '37-48'
        WHEN tenure_months BETWEEN 49 AND 60 THEN '49-60'
        WHEN tenure_months > 60 THEN '61+'
        ELSE 'Unknown'
    END AS tenure_range,
    churn_label
FROM sandbox.public.customer_churn)
select
    tenure_range,
    round(AVG(CASE WHEN churn_label = 'Yes' THEN 1.0 ELSE 0.0 END),4) AS churn_rate,
    COUNT(*) AS Count
from cte
GROUP BY tenure_range
ORDER BY tenure_range;


select 
count(*)/(select count(*) from sandbox.public.customer_churn),
churn_label
from sandbox.public.customer_churn
GROUP BY churn_label
ORDER BY churn_label;
--0.734630	FALSE
--0.265370	TRUE


select 
count(*),
churn_label
from sandbox.public.customer_churn
GROUP BY churn_label
ORDER BY churn_label;


SELECT 
    SENIOR_CITIZEN,
    AVG(CASE WHEN churn_label = 'Yes' THEN 1.0 ELSE 0.0 END)*100 AS Churn_Rate,
    COUNT(*) AS Count
FROM sandbox.public.customer_churn
GROUP BY SENIOR_CITIZEN
ORDER BY Churn_Rate DESC;
--SENIOR_CITIZEN	CHURN_RATE	COUNT
--TRUE	41.681300	1142
--FALSE	23.606200	5901

SELECT 
    churn_reason,
    count(*)
FROM sandbox.public.customer_churn
where churn_label = 'Yes'
GROUP BY churn_reason
ORDER BY count(*) DESC;
--SENIOR_CITIZEN	CHURN_RATE	COUNT
--TRUE	41.681300	1142
--FALSE	23.606200	5901


SELECT 
    INTERNET_SERVICE,
    AVG(CASE WHEN churn_label = 'Yes' THEN 1.0 ELSE 0.0 END)*100 AS Churn_Rate--,
    --COUNT(*) AS Count
FROM sandbox.public.customer_churn
GROUP BY INTERNET_SERVICE
ORDER BY Churn_Rate DESC;