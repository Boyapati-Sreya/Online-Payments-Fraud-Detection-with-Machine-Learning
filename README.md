# Online Payments Fraud Detection with Machine Learning
# FraudShield🛡️

This is a web application designed to detect fraudulent financial transactions using a pre-trained machine learning model. The app supports single transaction predictions and bulk predictions from a CSV file.

---
## Features
- **Single Prediction**: Analyze one transaction at a time.
- **Bulk Prediction**: Upload a CSV file containing transaction data for batch analysis.
- **Transaction History**: Review previously analyzed transactions.
- **User-Friendly Interface**: Built with Streamlit for simplicity.

---
### Steps

1. Clone this repository
   git clone https://github.com/Boyapati-Sreya/Online-Payments-Fraud-Detection-with-Machine-Learning.git
   cd Online-Payments-Fraud-Detection-with-Machine-Learning
   
   2.pip install -r requirements.txt

   3.pip install streamlit

   4.streamlit run app.py

---
This repository documents the milestones of the Online Payment Fraud Detection Project.

## Milestone 1 – Data Preprocessing

Loaded and inspected the raw dataset.

Handled missing values, removed duplicates.

Visualized transaction types & checked dataset balance.

Encoded categorical features & normalized numerical ones.

Saved the cleaned dataset and set up AWS S3 storage/retrieval.

## Milestone 2 & 3– Model Training & Deployment Preparation

Split preprocessed data into train/test sets.

Trained multiple models (Logistic Regression, Random Forest, XGBoost).

Tuned hyperparameters for optimal performance.

Evaluated models with accuracy, precision, recall, F1-score, ROC-AUC.

Compared results to select the best-performing model.

Packaged trained models and preprocessing steps (pickle/joblib).

Created reusable pipelines and artifacts for app integration.

## Milestone 4 – Streamlit Application

Built a web app (app.py) using Streamlit for fraud detection.

Key features:

Upload CSVs for bulk prediction.

Enter transaction details for single prediction.

Display clear fraud/non-fraud results with alerts.

Download processed results.

Integrated trained models for real-time predictions.
