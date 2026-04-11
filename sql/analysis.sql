CREATE TABLE processed_churn_train AS 
SELECT * FROM raw_churn_train;

SELECT COUNT(*) FROM processed_churn_train;

SELECT * 
FROM processed_churn_train
LIMIT 5;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'processed_churn_train'
ORDER BY ordinal_position;

SELECT DISTINCT "Subscription Type" FROM processed_churn_train;

SELECT DISTINCT "Contract Length" FROM processed_churn_train;

SELECT DISTINCT "Gender" FROM processed_churn_train;

