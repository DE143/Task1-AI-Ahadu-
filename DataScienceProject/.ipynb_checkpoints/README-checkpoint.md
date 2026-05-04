# Credit Scoring Model - Exploratory Data Analysis

## Project Overview

This project focuses on performing comprehensive Exploratory Data Analysis (EDA) on historical credit data to support inclusive finance and data-driven lending decisions in Ethiopia. The primary objective is to identify key risk factors that predict the likelihood of a borrower experiencing financial distress within the next two years.

The insights derived from this analysis will directly inform the development of a high-performing credit scoring model and its packaging as a scalable Model-as-a-Service (MaaS) API.

## Business Context

**Goal**: Predict borrower default risk to enable:
- More accurate credit risk assessment
- Data-driven lending decisions
- Financial inclusion for underserved populations
- Reduced default rates and improved portfolio performance

**Target Variable**: `SeriousDlqin2yrs` - Binary indicator of whether a borrower experienced 90+ days past due delinquency or worse within 2 years.

## Dataset Description

The dataset contains anonymized historical data from **150,000 borrowers** with the following features:

### Target Variable
- **SeriousDlqin2yrs**: Binary indicator (1 = experienced financial distress in next 2 years, 0 = otherwise)

### Borrower Demographics
- **age**: Age of the borrower in years
- **NumberOfDependents**: Number of dependents excluding the borrower

### Credit Utilization
- **RevolvingUtilizationOfUnsecuredLines**: Ratio of total balance on unsecured credit lines to total credit limits (values >1 indicate over-utilization)
- **NumberOfOpenCreditLinesAndLoans**: Total number of open credit lines and loans

### Payment History
- **NumberOfTime30-59DaysPastDueNotWorse**: Count of times 30-59 days past due in last 2 years
- **NumberOfTime60-89DaysPastDueNotWorse**: Count of times 60-89 days past due in last 2 years
- **NumberOfTimes90DaysLate**: Count of times 90+ days past due

### Financial Metrics
- **DebtRatio**: Monthly debt payments divided by monthly gross income
- **MonthlyIncome**: Monthly gross income in local currency
- **NumberRealEstateLoansOrLines**: Number of mortgage and real estate loans (including home equity lines)

### Identifier
- **Unnamed: 0**: Unique borrower ID (row index)

## Project Structure

```
DataScienceProject/
├── data/                      # Dataset files
│   └── cs-training.csv       # Credit scoring training dataset
├── notebooks/                 # Jupyter notebooks for analysis
│   └── eda_analysis.ipynb    # Main EDA notebook
    └── 01_data_loading_and_review.ipynb
├── src/                      # Python source code
│   └── eda_utils.py          # Utility functions for EDA
├── outputs/                  # Generated plots and reports
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Key Analysis Areas

1. **Data Quality Assessment**
   - Missing value analysis and imputation strategies
   - Outlier detection and treatment
   - Data type validation and corrections

2. **Univariate Analysis**
   - Distribution analysis of numerical features
   - Frequency analysis of categorical features
   - Target variable class imbalance assessment

3. **Bivariate Analysis**
   - Relationship between features and target variable
   - Statistical significance testing
   - Risk factor identification

4. **Multivariate Analysis**
   - Correlation analysis between features
   - Feature interaction patterns
   - Multicollinearity detection

5. **Feature Engineering**
   - Derived risk indicators
   - Binning and categorization
   - Feature transformation recommendations

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Launch Jupyter Notebook:
```bash
jupyter notebook
```

3. Open and run `notebooks/eda_analysis.ipynb`

## Expected Outcomes

- Comprehensive understanding of borrower risk profiles
- Identification of key predictive features for credit scoring
- Data quality recommendations for model development
- Feature engineering strategies for improved model performance
- Statistical insights to support business decision-making

## Next Steps

After completing the EDA:
1. Feature engineering and selection
2. Model development (Logistic Regression, Random Forest, XGBoost, etc.)
3. Model evaluation and validation
4. Model deployment as MaaS API
5. Monitoring and maintenance framework
