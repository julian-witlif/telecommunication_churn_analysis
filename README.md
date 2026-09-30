# Telecommunications Customer Churn Analysis

This portfolio project analyzes 7,043 telecom customer records to identify churn patterns and prioritize customers for retention review. SQL explores differences across customer segments; a logistic regression model in Python produces churn scores from customer, service, contract, and billing attributes.

On a held-out test set, the model achieved a ROC AUC of 0.853. The highest-scoring 10% contained 27.5% of the test set's recorded churners. The proposed next step is time-based validation followed by a randomized retention pilot; no intervention impact has been measured.

- [SQL exploration](exploratory_analysis_gathering_stats.sql)
- [Python churn model](churn_model_logistic_regression.py)
- [Excel visualization](Excel%20Visualisation.xlsx)
