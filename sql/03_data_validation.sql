-- 1. Row count check
SELECT COUNT(*) FROM processed_churn_train;

-- 2. Sample data preview
SELECT * 
FROM processed_churn_train
LIMIT 5;

SELECT COUNT(*) - COUNT(DISTINCT "CustomerID") AS duplicate_count
FROM processed_churn_train;

-- 3. Schema validation
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'processed_churn_train'
ORDER BY ordinal_position;

-- 4. Categorical value checks
SELECT DISTINCT "Subscription Type" FROM processed_churn_train;

SELECT DISTINCT "Contract Length" FROM processed_churn_train;

SELECT DISTINCT "Gender" FROM processed_churn_train;

-- 5. Age value checks
SELECT 
    MIN("Age") AS min_age, 
    MAX("Age") AS max_age, 
    AVG("Age") AS avg_age   
FROM processed_churn_train;
