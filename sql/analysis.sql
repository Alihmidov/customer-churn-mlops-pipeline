-- Female customers show significantly higher churn rates compared to males (66.67% vs 49.13%).
-- This indicates "Gender" is a strong predictive feature for the model.
SELECT 
	"Gender",
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Gender";
-- Gender | total  | churn_rate

-- female | 190580 | 66.67%
-- male   | 250252 | 49.13%

-----------------------------------------------------------------------------------------------------------------------

-- Older customers (Age > 50) have a 100% churn rate, while younger groups show much lower rates (55.52% and 42.95%).
-- This extreme outlier suggests that "Age" is a critical factor or indicates a specific data segment issue.
SELECT
    CASE 
        WHEN "Age" < 30 THEN 'Young'
        WHEN "Age" BETWEEN 30 AND 50 THEN 'Middle-aged'
        ELSE 'Old'
    END AS age_group,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY age_group
ORDER BY churn_rate DESC;
-- age_group   | total  | churn_rate

-- Old         | 81654  | 100.00%
-- Young       | 112026 | 55.52%
-- Middle-aged | 247152 | 42.95%

-----------------------------------------------------------------------------------------------------------------------

-- Churn rate hits 100% when SupportCalls exceed a specific threshold for each age group:
-- Young (>2 calls), Middle-aged (>5 calls), and Old (all calls show 100% churn).
-- This suggests "SupportCalls" is a critical feature with age-dependent impact.
-- This logic will be used for Feature Engineering in Python to boost model sensitivity.
SELECT 
    CASE 
        WHEN "Age" < 30 THEN 'Young'
        WHEN "Age" BETWEEN 30 AND 50 THEN 'Middle-aged'
        ELSE 'Old'
    END AS age_group,
    "Support Calls",
    COUNT(*) AS total_customers,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY age_group, "Support Calls"
ORDER BY age_group, "Support Calls" ASC;
-- age_group   | Support Calls | total    | churn_rate

-- Middle-aged | 0 - 3         | ~39.5K ea| 21.61% ... 21.99%
-- Middle-aged | 4             | 25439    | 36.78%
-- Middle-aged | 5             | 11711    | 88.75%
-- Middle-aged | 6 - 10        | ~10.3K ea| 100.00%
-- Old         | 0 - 10        | ~7.4K ea | 100.00% (Critical)
-- Young       | 0 - 2         | ~21.6K ea| 22.03% ... 25.70%
-- Young       | 3 - 10        | ~5.9K ea | 100.00% (Critical)

-----------------------------------------------------------------------------------------------------------------------

-- Monthly contract holders exhibit a 100% churn rate, 
-- significantly higher than annual (46.08%) and quarterly (46.03%) plans.
-- This suggests "Contract Length" is a deterministic predictor for churn in this dataset.
SELECT 
    "Contract Length",
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate_pct
FROM processed_churn_train
GROUP BY "Contract Length"
ORDER BY churn_rate_pct DESC;
-- Contract Length | total  | churn_rate

-- monthly         | 87104  | 100.00%
-- annual          | 177198 | 46.08%
-- quarterly       | 176530 | 46.03%

-----------------------------------------------------------------------------------------------------------------------

-- Monthly contracts are identified as a deterministic 'high_churn_risk' group (100% churn).
-- This logic will be used for Feature Engineering in Python to boost model sensitivity.
SELECT 
    CASE 
        WHEN "Contract Length" = 'monthly' THEN 'high_churn_risk'
        ELSE 'lower_risk'
    END AS contract_risk,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate_pct
FROM processed_churn_train
GROUP BY contract_risk
ORDER BY churn_rate_pct;
-- contract_risk     | total  | churn_rate

-- lower_risk        | 353728 | 46.05%
-- high_churn_risk   | 87104  | 100.00%

-----------------------------------------------------------------------------------------------------------------------

-- Monthly contracts are a 100% churn risk for everyone. 
-- However, 'Old' customers also show very high churn (~87%) on annual/quarterly plans.
-- Plan: Use this to create a 'risk_score' feature in Python.
SELECT 
    CASE 
        WHEN "Age" >= 50 THEN 'Old'
        ELSE 'Not Old'
    END as age_status,
    "Contract Length",
    COUNT(*) as total,
    ROUND(AVG("Churn") * 100, 2) as churn_rate
FROM processed_churn_train
GROUP BY age_status, "Contract Length"
ORDER BY age_status, churn_rate DESC;
-- age_status | Contract Length | total  | churn_rate

-- Not Old    | monthly         | 57878  | 100.00%
-- Not Old    | annual          | 144193 | 36.72%
-- Not Old    | quarterly       | 143580 | 36.69%
-- Old        | monthly         | 29226  | 100.00%
-- Old        | annual          | 33005  | 86.95%
-- Old        | quarterly       | 32950  | 86.70%

-----------------------------------------------------------------------------------------------------------------------

-- Churn rates are nearly identical across all subscription types (~56-58%).
-- This feature has low predictive power, so no specific feature engineering is required here.
SELECT 
    "Subscription Type",
    COUNT(*) AS total,
    SUM("Churn") AS churned,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate_pct
FROM processed_churn_train
GROUP BY "Subscription Type"
ORDER BY churn_rate_pct DESC;
-- Subscription Type | total  | churned | churn_rate

-- basic             | 143026 | 83210   | 58.18%
-- standard          | 149128 | 83616   | 56.07%
-- premium           | 148678 | 83173   | 55.94%

-----------------------------------------------------------------------------------------------------------------------

-- Churn increases sharply with more support calls, hitting 100% at 6+ calls.
-- This shows a clear link between customer service issues and churn.
SELECT 
    "Support Calls",
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Support Calls"
ORDER BY "Support Calls";
-- Support Calls | total | churn_rate

-- 0              | 69875 | 30.28%
-- 1              | 69476 | 30.36%
-- 2              | 66571 | 31.55%
-- 3              | 52729 | 41.64%
-- 4              | 38750 | 58.50%
-- 5              | 24918 | 94.71%
-- 6              | 23554 | 100.00%
-- 7              | 23870 | 100.00%
-- 8              | 23559 | 100.00%
-- 9              | 23630 | 100.00%
-- 10             | 23900 | 100.00%

-----------------------------------------------------------------------------------------------------------------------

-- Grouping support calls into risk levels based on observed churn thresholds.
-- Plan: Use these 'low', 'medium', and 'high' risk categories for Feature Engineering.
SELECT
	CASE 
    	WHEN "Support Calls" <= 2 THEN 'low_risk'
	    WHEN "Support Calls" <= 4 THEN 'medium_risk'
    	ELSE 'high_risk'
	END AS support_call_risk,
	COUNT(*) AS total,  
	ROUND(AVG("Churn") * 100, 2) as churn_rate
FROM processed_churn_train
GROUP BY support_call_risk
ORDER BY churn_rate;
-- support_call_risk | total  | churn_rate

-- low_risk          | 205922 | 30.72%
-- medium_risk       | 91479  | 48.78%
-- high_risk         | 143431 | 99.08%

-----------------------------------------------------------------------------------------------------------------------

-- Dividing tenure into 4 stages based on churn fluctuations:
-- 1. Initial High Risk (1-5 months)
-- 2. First Stabilization (6-11 months)
-- 3. Renewal Risk Period (12-24 months)
-- 4. Long-term Retention (25+ months)
SELECT 
    "Tenure",
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Tenure"
ORDER BY "Tenure";
-- Result:
-- Tenure            | total    | churn_rate

-- 1 - 5 (Initial)   | ~6.5K ea | 63.44% ... 65.37%
-- 6 - 11 (Stab.)    | ~7.6K ea | 53.53% ... 55.33%
-- 12 - 24 (Renewal) | ~6.6K ea | 62.02% ... 64.49%
-- 25 - 60 (Loyalty) | ~7.6K ea | 53.01% ... 55.38%

-----------------------------------------------------------------------------------------------------------------------

-- Tenure shows a non-linear churn trend with two major risk peaks.
-- Churn spikes during the first 5 months and again during the 12-24 month 'Renewal Risk' phase.
-- Plan: Create 'tenure_segment' in Python to help the model identify these specific risk cycles.
SELECT 
	CASE 
		WHEN "Tenure" <= 5 THEN '1_Initial_High_Risk'
		WHEN "Tenure" <= 11 THEN '2_First_Stabilization'
		WHEN "Tenure" <= 24 THEN '3_Renewal_Risk'
		ELSE '4_Long_term_Loyalty'
	END AS tenure_segment,
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY tenure_segment
ORDER BY tenure_segment;
-- tenure_segment        | total  | churn_rate

-- 1_Initial_High_Risk   | 32674  | 64.43%
-- 2_First_Stabilization  | 45822  | 54.19%
-- 3_Renewal_Risk        | 86600  | 63.18%
-- 4_Long_term_Loyalty   | 275736 | 54.18%

-----------------------------------------------------------------------------------------------------------------------

-- Observation: Churn rate drops from ~61% to ~55% when usage frequency reaches 10 or more.
-- Plan: Create a binary 'is_active_user' feature (Usage >= 10) to help the model distinguish loyal users.
SELECT 
    "Usage Frequency", 
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Usage Frequency"
ORDER BY "Usage Frequency";
-- Usage Frequency  | total   | churn_rate

-- 1 - 9            | ~13K ea | 59.84% ... 62.18%
-- 10 - 30          | ~15K ea | 54.26% ... 55.59%

----------------------------------------------------------------------------------------------------------------------

-- Usage frequency has a clear tipping point at 10 monthly uses.
-- Creating 'usage_intensity' to distinguish between 'Low Usage' (61.37% churn) and 'Regular Usage' (54.90% churn).
-- Plan: Implement this as a binary feature in Python to enhance model predictive power.
SELECT 
	CASE 
		WHEN "Usage Frequency" <= 9 THEN 'Low Usage'
    	ELSE 'Regular Usage' 
	END AS usage_intensity,
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY usage_intensity
ORDER BY churn_rate DESC;
-- usage_intensity   | total  | churn_rate

-- Low Usage         | 123334 | 61.37%
-- Regular Usage     | 317498 | 54.90%

-----------------------------------------------------------------------------------------------------------------------

-- Churn reaches 100% when payment delay exceeds 20 days.
-- This indicates a critical threshold for service termination or customer loss.
-- Plan: Create a binary 'is_payment_overdue' feature in Python to capture this 100% risk segment.
SELECT 
    "Payment Delay",
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Payment Delay"
ORDER BY "Payment Delay";
-- Payment Delay    | total  | churn_rate

-- 0 - 20           | ~17K ea| 45.78% ... 46.56%
-- 21 - 30          | ~8K ea | 100.00% (Critical)

-----------------------------------------------------------------------------------------------------------------------

-- Payment delay shows a 100% churn trigger after 20 days.
-- Segmenting into 'On-time' and 'Critical Delay' to capture this risk boundary.
SELECT 
    CASE 
        WHEN "Payment Delay" <= 20 THEN 'On-time'
        ELSE 'Critical Delay' 
    END AS payment_status,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY payment_status
ORDER BY churn_rate ASC;
-- payment_status   | total  | churn_rate

-- On-time          | 356802 | 46.52%
-- Critical Delay   | 84030  | 100.00%

-----------------------------------------------------------------------------------------------------------------------

-- Customers spending less than 500 have a 100% churn rate.
-- This is a critical financial limit for keeping customers.
-- Goal: Use this 500 threshold to flag high-risk users in the model.
SELECT 
    CASE 
        WHEN "Total Spend" < 500 THEN 'Low Spender (0-500)'
        ELSE 'High Spender (500+)'
    END AS spending_group,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY spending_group
ORDER BY churn_rate DESC;
-- spending_group       | total  | churn_rate

-- Low Spender (0-500)  | 115796 | 100.00%
-- High Spender (500+)  | 325036 | 41.29%

-----------------------------------------------------------------------------------------------------------------------

-- Analyzing churn sensitivity based on the timing of the last customer interaction.
-- Observation: A clear 'fatigue point' exists at 15 days; churn jumps by ~17% beyond this mark.
-- Goal: Identify these 'cold' users so the model can flag them earlier.
SELECT 
    "Last Interaction",
	COUNT(*) AS total,
	ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY "Last Interaction"
ORDER BY "Last Interaction";
-- Last Interaction | total    | churn_rate

-- 1 - 15 (Active)   | ~16.7K ea| 48.81% ... 49.64%
-- 16 - 30 (Dormant) | ~12.7K ea| 66.13% ... 66.93%

-----------------------------------------------------------------------------------------------------------------------

-- Churn risk increases significantly after 15 days of inactivity (from ~49% to ~66%).
-- Feature Engineering: Creating 'interaction_recency' to distinguish between 'Active' and 'Dormant' users.
SELECT 
    CASE 
        WHEN "Last Interaction" <= 15 THEN 'Active Interest'
        ELSE 'Dormant/Cold' 
    END AS interaction_recency,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY interaction_recency
ORDER BY churn_rate ASC;
-- interaction_recency | total  | churn_rate

-- Active Interest     | 250395 | 49.27%
-- Dormant/Cold        | 190437 | 66.50%

-----------------------------------------------------------------------------------------------------------------------

-- Analyzing the interaction between Customer Support engagement and Recency.
-- Observation 1: 'Support Calls' is the dominant predictor. If calls > 4, churn is almost certain (~99%), regardless of 'Last Interaction'.
-- Observation 2: 'Last Interaction' only matters for satisfied customers (Low Calls). 'Cold' users in this group are 1.5x more likely to churn (46.76% vs 29.28%).
-- Strategy: Prioritize high-call users for immediate intervention and target 'Cold/Low-Call' users with re-engagement campaigns.
SELECT 
    CASE WHEN "Last Interaction" > 15 THEN 'Cold' ELSE 'Active Interest' END AS interaction_status,
    CASE WHEN "Support Calls" > 4 THEN 'High Calls' ELSE 'Low Calls' END AS call_status,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY interaction_status, call_status
ORDER BY churn_rate DESC;
-- interaction_status | call_status | total  | churn_rate

-- Cold               | High Calls  | 71418  | 99.39%
-- Active Interest    | High Calls  | 72013  | 98.78%
-- Cold               | Low Calls   | 119019 | 46.76%
-- Active Interest    | Low Calls   | 178382 | 29.28%

-----------------------------------------------------------------------------------------------------------------------

-- Payment Delay > 20 is a deterministic churn trigger (100%), overriding all usage behaviors.
-- Observation: High usage does not prevent churn once the critical payment threshold is crossed.
-- Insight: Usage frequency only influences churn risk for on-time payers (~7% difference).
-- Strategy: Use this binary logic for 'is_payment_risk' feature engineering in Python.
SELECT 
    CASE WHEN "Payment Delay" <= 20 THEN 'on-time' ELSE 'Critical Delay' END AS payment_status,
    CASE WHEN "Usage Frequency" <= 9 THEN 'Low Usage' ELSE 'High Usage' END AS usage_status,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY payment_status, usage_status
ORDER BY churn_rate DESC;
-- payment_status  | usage_status | total  | churn_rate

-- Critical Delay  | High Usage   | 58769  | 100.00%
-- Critical Delay  | Low Usage    | 25261  | 100.00%
-- on-time         | Low Usage    | 98073  | 51.42%
-- on-time         | High Usage   | 258729 | 44.66%

-----------------------------------------------------------------------------------------------------------------------

-- Checking if a long-term relationship helps when there are many problems.
-- Fact 1: Too many support calls (5+) always lead to churn (~99%). 
--         Even if the customer has been with us for 2 years, they still leave.
-- Fact 2: Having a long tenure only helps if everything is going well. 
--         Among happy customers, long-term ones are 10% more loyal than new ones.
-- Result: A long history with the company does NOT fix bad service. 
--         A few bad experiences are enough to lose even the most loyal customer.
SELECT 
    CASE 
        WHEN "Tenure" <= 5 THEN '1_Initial_High_Risk'
        WHEN "Tenure" <= 11 THEN '2_First_Stabilization'
        WHEN "Tenure" <= 24 THEN '3_Renewal_Risk'
        ELSE '4_Long_term_Loyalty'
    END AS tenure_status,
    CASE WHEN "Support Calls" > 4 THEN 'High Calls' ELSE 'Low Calls' END AS call_status,
    COUNT(*) AS total,
    ROUND(AVG("Churn") * 100, 2) AS churn_rate
FROM processed_churn_train
GROUP BY tenure_status, call_status
ORDER BY tenure_status, churn_rate DESC;
-- tenure_status          | call_status | total  | churn_rate

-- 1_Initial_High_Risk    | High Calls  | 11847  | 99.38%
-- 1_Initial_High_Risk    | Low Calls   | 20827  | 44.56%
-- 2_First_Stabilization  | High Calls  | 14449  | 98.93%
-- 2_First_Stabilization  | Low Calls   | 31373  | 33.59%
-- 3_Renewal_Risk         | High Calls  | 31039  | 99.18%
-- 3_Renewal_Risk         | Low Calls   | 55561  | 43.07%
-- 4_Long_term_Loyalty    | High Calls  | 86096  | 99.03%
-- 4_Long_term_Loyalty    | Low Calls   | 189640 | 33.82%