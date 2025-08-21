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


# Function to load the trained model
def load_model():
    try:
        model_path = r"C:\Users\BABITA\Desktop\fraud detection\Milestone_4\models\Random_forest_model.pkl"
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
        'type_CASH_IN': [1 if transaction_type_code == 1 else 0],
        'type_DEBIT': [1 if transaction_type_code == 2 else 0],
        'type_PAYMENT': [1 if transaction_type_code == 3 else 0],
        'type_TRANSFER': [1 if transaction_type_code == 4 else 0]
    })

    prediction = model.predict(input_data)
    result = "Fraud" if prediction[0] == 1 else "Not Fraud"

    # ✅ Post-rule correction: check transaction math
    # For outflows (CASH_OUT, PAYMENT, DEBIT, TRANSFER):
    if transaction_type_code in [0, 2, 3, 4]:
        if abs((oldbalanceOrg - newbalanceOrig) - amount) < 1e-2:
            result = "Not Fraud"

    # For inflows (CASH_IN):
    if transaction_type_code == 1:
        if abs((newbalanceOrig - oldbalanceOrg) - amount) < 1e-2:
            result = "Not Fraud"

    return result


# Single Prediction Page
def single_prediction_page():
    centered_title("Prediction of Fraud Transactions")
    st.write("Enter transaction details below to check for potential fraud.")
    st.write(" Note: Negative values are not allowed.")
    
    # Input fields
    amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f", value=0.0)
    oldbalanceOrg = st.number_input("Old Balance Amount", min_value=0.0, format="%.2f", value=0.0)
    newbalanceOrig = st.number_input("New Balance Amount", min_value=0.0, format="%.2f", value=0.0)
    transaction_type = st.radio("Transaction Type", ["CASH_OUT", "CASH_IN", "DEBIT", "PAYMENT", "TRANSFER"], horizontal=True)

    # Check if inputs are provided and valid
    if st.button("Submit"):
        if amount <= 0.0 or oldbalanceOrg <= 0.0 or newbalanceOrig < 0.0 or transaction_type == "":
            st.error("Please enter valid values for all required fields.")\
            
        else:
            # Transaction type mapping
            transaction_type_code = {"CASH_OUT": 0, "CASH_IN": 1, "DEBIT": 2, "PAYMENT": 3, "TRANSFER": 4}[transaction_type]
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
                background-image: url('https://i.postimg.cc/DftnCv7D/Image12345.jpg');
                background-size: cover;
                background-position: center;
                height: 100vh; 
            }
            .blurred-box {
                backdrop-filter: blur(10px); 
                border-radius: 10px;
                padding: 30px;
                max-width: 80%; 
                margin: 50px auto; 
                text-align: center;
                color: white; 
            }
            .blurred-box h1, .blurred-box h2, .blurred-box h3 {
                font-size: 40px;  
                margin-bottom: 15px;
            }
            .blurred-box p {
                font-size: 18px;
                line-height: 1.8;
                margin-bottom: 20px;
            }
        </style>
         <div class="blurred-box">
            <h1>Welcome to FraudShield 🛡️</h1>
            <h3>Your Trusted Companion for Safe and Secure Transactions </h3>
            <p>
                This web application is designed to help users detect potential fraudulent transactions 
                using a pre-trained machine learning model. It provides both single and bulk prediction functionalities, 
                allowing you to assess transactions individually or by batch.
            </p>
            <h3>Why Fraud Detection Matters </h3>
            <p>
                Online payment fraud is becoming more prevalent, leading to significant financial losses 
                for individuals and businesses alike. Detecting fraud in real time can help protect your finances and 
                build trust in digital transactions.
            </p>
            <h3>How Does FraudShield Work? </h3>
            <p>
                Our system uses advanced machine learning algorithms to identify potentially fraudulent transactions. 
                Here's how it works:
            </p>
            <p>
                <strong>Data Collection</strong>: Real-time transaction data, including user details, amounts, and payment methods, is gathered.<br>
                <strong>Pattern Analysis</strong>: Irregular patterns like mismatched locations or unusual spending behaviors are identified.<br>
                <strong>Risk Scoring</strong>: Transactions are assigned a risk score based on frequency, size, and past behaviors.<br>
                <strong>Flagging</strong>: Suspicious transactions are flagged for review or blocked to prevent fraud.
            </p>
            <h3>Key Features </h3>
            <p>
                Single Prediction allows you to manually enter transaction details for immediate feedback.<br>
                File Prediction enables bulk analysis of transactions from a CSV file.<br>
                A log of previously analyzed transactions ensures easy tracking.<br>
                Fraud Alerts provide real-time warnings for risky transactions.
            </p>
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
    - Email: sreyaboyapati@gmail.com
    - LinkedIn: [LinkedIn](https://www.linkedin.com/in/sreya-boyapati?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
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
    st.write(" *Note: File must be in CSV format.*")
    model = load_model()
    if model is not None:
        uploaded_file = st.file_uploader("Upload CSV File")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())

            # ✅ Mapping dictionary for transaction types
            type_mapping = {
                "CASH_OUT": 0,
                "CASH_IN": 1,
                "DEBIT": 2,
                "PAYMENT": 3,   # fixed, not 2
                "TRANSFER": 4
            }

            if st.button("Predict All"):
                # Convert type column from string → numeric codes
                df['Prediction'] = df.apply(
                    lambda row: predict_fraud(
                        model,
                        row['amount'],
                        row['oldbalanceOrg'],
                        row['newbalanceOrig'],
                        type_mapping[row['type']]
                    ),
                    axis=1
                )

                # Save predictions in session state
                st.session_state.file_predictions = pd.concat(
                    [st.session_state.file_predictions,
                     df[["amount", "oldbalanceOrg", "newbalanceOrig", "type", "Prediction"]]],
                    ignore_index=True
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