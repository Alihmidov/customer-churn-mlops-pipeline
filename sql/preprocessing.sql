ALTER TABLE processed_churn_train
ALTER COLUMN "CustomerID" TYPE INTEGER USING ("CustomerID"::integer),
ALTER COLUMN "Churn" TYPE INTEGER USING ("Churn"::integer),
ALTER COLUMN "Age" TYPE INTEGER USING ("Age"::integer),
ALTER COLUMN "Support Calls" TYPE INTEGER USING ("Support Calls"::integer),
ALTER COLUMN "Payment Delay" TYPE INTEGER USING ("Payment Delay"::integer);
