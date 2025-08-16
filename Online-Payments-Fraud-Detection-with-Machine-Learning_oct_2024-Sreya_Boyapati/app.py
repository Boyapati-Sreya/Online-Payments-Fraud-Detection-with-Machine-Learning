import streamlit as st
import pickle
import pandas as pd

# Set the page to a wide layout
st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.markdown(
    """
    <style>
        div.stButton > button {
            width: 250px; /* Fixed width for all buttons */
            height: 50px; /* Fixed height for all buttons */
            font-size: 16px; /* Adjust font size */
            margin: 5px auto; /* Center buttons in each column */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# session state for page navigation and data history
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "data_history" not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=["Amount", "Old Balance", "New Balance", "Type", "Result"])
if "single_predictions" not in st.session_state:
    st.session_state.single_predictions = pd.DataFrame(columns=["Amount", "Old Balance", "New Balance", "Type", "Result"])
if "file_predictions" not in st.session_state:
    st.session_state.file_predictions = pd.DataFrame(columns=["amount", "oldbalanceOrg", "newbalanceOrig", "type", "Prediction"])

def set_page(new_page):
    st.session_state.page = new_page

def centered_title(title):
    st.markdown(f"<h1 style='text-align: center; font-size: 36px;'>{title}</h1>", unsafe_allow_html=True)

nav_labels = ["🏠 Home", "🔍 Single Prediction", "📄 File Prediction", "📜 Transaction History", "ℹ About Us"]
nav_pages = ["Home", "Single Prediction", "File Prediction", "Transaction History", "About Us"]
with st.container():
    cols = st.columns(len(nav_labels))  
    for col, label, page in zip(cols, nav_labels, nav_pages):
        if col.button(label): 
            set_page(page)

st.markdown("---")

# Function to load the trained model
def load_model():
    try:
        model_path = r"C:\Users\BABITA\Desktop\Fraud_detection_app\models\Random_forest_model.pkl"
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {model_path}. Please ensure the file exists.")
        return None

# Fraud prediction logic
def predict_fraud(model, amount, oldbalanceOrg, newbalanceOrig, transaction_type_code):
    input_data = pd.DataFrame({
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'type_CASH_OUT': [1 if transaction_type_code == 0 else 0],
        'type_DEBIT': [1 if transaction_type_code == 1 else 0],
        'type_PAYMENT': [1 if transaction_type_code == 2 else 0],
        'type_TRANSFER': [1 if transaction_type_code == 3 else 0]
    })
    prediction = model.predict(input_data)
    return "Fraud" if prediction[0] == 1 else "Not Fraud"

# Single Prediction Page
def single_prediction_page():
    centered_title("Prediction of Fraud Transactions")
    st.write("Enter transaction details below to check for potential fraud.")
    st.write(" Note: Negative values are not allowed.")
    
    # Input fields
    amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f", value=0.0)
    oldbalanceOrg = st.number_input("Old Balance Amount", min_value=0.0, format="%.2f", value=0.0)
    newbalanceOrig = st.number_input("New Balance Amount", min_value=0.0, format="%.2f", value=0.0)
    transaction_type = st.radio("Transaction Type", ["CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"], horizontal=True)

    # Check if inputs are provided and valid
    if st.button("Submit"):
        if amount <= 0.0 or oldbalanceOrg <= 0.0 or newbalanceOrig < 0.0 or transaction_type == "":
            st.error("Please enter valid values for all required fields.")
        else:
            # Transaction type mapping
            transaction_type_code = {"CASH_OUT": 0, "DEBIT": 1, "PAYMENT": 2, "TRANSFER": 3}[transaction_type]
            model = load_model()
            
            if model:
                result = predict_fraud(model, amount, oldbalanceOrg, newbalanceOrig, transaction_type_code)
                
                # Save transaction
                new_transaction = pd.DataFrame([{
                    "Amount": amount,
                    "Old Balance": oldbalanceOrg,
                    "New Balance": newbalanceOrig,
                    "Type": transaction_type,
                    "Result": result
                }])
                
                st.session_state.single_predictions = pd.concat([st.session_state.single_predictions, new_transaction], ignore_index=True)
                if result == "Fraud":
                    st.warning("⚠ Potential Fraud Detected!")
                else:
                    st.success("✅ Transaction appears normal.")
                
                st.subheader("Transaction Details")
                st.table(new_transaction)

                
#Home page
def home_page():
    st.markdown(
        """
        <style>
            .stApp {
                background-image: url('https://imgur.com/vxU5Ubk.jpg'); /* Replace with your image URL */
                background-size: cover;
                background-position: center;
                height: 100vh;  /* Ensure it covers the entire screen */
            }
            .blurred-box {
                backdrop-filter: blur(10px); /* Apply blur effect */
                border-radius: 10px;
                padding: 30px;
                max-width: 100%;  /* Make box span the full width */
                margin: 30px 0 50px 0;  /* Move box up by reducing top margin */
                text-align: center;
                color: white; /* Ensure text is visible against background */
            }
            .blurred-box h1 {
                font-size: 36px;  /* Customize heading size */
                margin-bottom: 20px;
            }
            .blurred-box p {
                font-size: 18px;
                line-height: 1.6;
            }
            .blurred-box ul {
                text-align: left;
                font-size: 18px;
            }
        </style>
        <div class="blurred-box">
            <h1>Online Payment Fraud Detection System</h1>
            <p>This web application is designed to help users detect potential fraudulent transactions using a pre-trained machine learning model.
            It provides both single and bulk prediction functionalities, allowing you to assess transactions individually or by batch.</p>
            <h3>Key Features</h3>
            <ul>
                <li><strong>Single Prediction</strong>: Enter transaction details manually to get immediate feedback.</li>
                <li><strong>File Prediction</strong>: Upload a CSV file for batch transaction analysis.</li>
                <li><strong>View Past Transactions</strong>: Access a log of previously processed transactions with results.</li>
                <li><strong>Fraud Alerts</strong>: Receive real-time warnings for potentially fraudulent transactions.</li>
            </ul>
            <h3>Why Choose Us for Online Payment Fraud Detection?</h3>
            <p>Our Online Payment Fraud Detection System offers a powerful and easy-to-use solution to detect fraudulent transactions, leveraging machine learning for accurate predictions.</p>
            <h3>How to Prevent Online Payment Fraud</h3>
            <ul>
                <li><strong>Use Secure Payment Gateways</strong>: Ensure transactions are encrypted using <strong>SSL</strong> or <strong>TLS</strong> protocols to protect sensitive information.</li>
                <li><strong>Implement Multi-Factor Authentication (MFA)</strong>: Add an extra layer of security by requiring a second form of identification, like a phone code or fingerprint.</li>
                <li><strong>Monitor Transaction Patterns</strong>: Use machine learning to analyze transactions for unusual behavior, such as large purchases or changes in buying patterns.</li>
                <li><strong>Use Address Verification System (AVS)</strong>: Check the customer’s billing address against the one on file with their card issuer to verify legitimacy.</li>
                <li><strong>Ensure PCI Compliance</strong>: Follow <strong>PCI DSS</strong> standards to securely store and handle payment data, protecting both businesses and customers from fraud.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# About Us Page
def about_us_page():
    centered_title("About Us")
    
    st.write("""
    ### Our Mission
    Our mission is to create an accessible and reliable tool for detecting fraud in online financial transactions. By leveraging advanced machine learning techniques, we aim to empower users with real-time fraud detection and predictive analytics. This project is designed with ease of use in mind, ensuring that both technical and non-technical users can confidently assess transaction risks and protect their financial data.

    Additionally, our goal is to provide a reliable and user-friendly tool for detecting fraud in financial transactions, offering both single and bulk prediction functionalities. We strive to make the detection process efficient, intuitive, and secure, allowing users to safeguard their finances effectively.

    ### The Problem We Solve
    Financial fraud is a growing concern worldwide, causing significant losses for businesses and consumers alike. 
    Our fraud detection system helps identify potentially fraudulent transactions in real-time, improving security and minimizing risk.

    ### Our Approach
    Using a well-balanced dataset with features like transaction type, old and new bank balances, and fraud status, our model is trained to detect fraudulent behavior accurately.

    ### Benefits of Using Our Tool
    - Real-time Fraud Detection: Instantly identifies suspicious transactions.
    - User-Friendly Interface: Accessible and easy-to-use for non-technical users.
    - Scalable Solution: Designed to handle large volumes of financial data efficiently.

    ### Contact Us
    - GitHub: [Github](https://github.com/Boyapati-Sreya)
    - Email: ABC@fraud-detection.com
    - LinkedIn: [LinkedIn](www.linkedin.com/in/sreya-boyapati)
    """)


# Transaction History Page
def transaction_history_page():
    centered_title("Transaction History")
    
    if "single_predictions" in st.session_state:
        single_predictions = st.session_state.single_predictions
        if not single_predictions.empty:
            st.subheader("Single Prediction History")
            st.dataframe(single_predictions)
        else:
            st.write("No single prediction history available.")
    
    if "file_predictions" in st.session_state:
        file_predictions = st.session_state.file_predictions
        if not file_predictions.empty:
            st.subheader("File Prediction History")
            st.dataframe(file_predictions)
        else:
            st.write("No file prediction history available.")

# File Prediction Page
def file_prediction_page():
    centered_title("File Prediction")
    st.write("Upload a CSV file containing transaction details for bulk prediction.")
    st.write(" **Note: File must be in CSV format.**")
    model = load_model()
    if model is not None:
        uploaded_file = st.file_uploader("Upload CSV File")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())
            if st.button("Predict All"):
                df['Prediction'] = df.apply(lambda row: predict_fraud(model, row['amount'], row['oldbalanceOrg'], row['newbalanceOrig'], row['type']), axis=1)
                st.session_state.file_predictions = pd.concat(
                    [st.session_state.file_predictions, df[["amount", "oldbalanceOrg", "newbalanceOrig", "type", "Prediction"]]], ignore_index=True
                )
                
                st.success("Bulk prediction completed!")
                st.dataframe(df)

# Main Program Flow/nagivation
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Single Prediction":
    single_prediction_page()
elif st.session_state.page == "File Prediction":
    file_prediction_page()
elif st.session_state.page == "Transaction History":
    transaction_history_page()
elif st.session_state.page == "About Us":
    about_us_page()