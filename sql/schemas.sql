-- Müştəri məlumatları cədvəlinin strukturu
CREATE TABLE IF NOT EXISTS raw_churn_train (
    "CustomerID" TEXT,
    "Age" INT,
    "Gender" TEXT,
    "Tenure" INT,
    "Usage Frequency" INT,
    "Support Calls" INT,
    "Payment Delay" INT,
    "Subscription Type" TEXT,
    "Contract Length" TEXT,
    "Total Spend" FLOAT,
    "Last Interaction" INT,
    "Churn" INT
);