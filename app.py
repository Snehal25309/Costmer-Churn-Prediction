import streamlit as st
import pickle as pkl
import pandas as pd
import os
import gdown
import joblib

FILE_ID = "1aDsOev9d0C8osAHO0LYScAuamsk50mU3"
OUTPUT = "model.joblib"

if not os.path.exists(OUTPUT):
    gdown.download(
    f"https://drive.google.com/uc?export=download&id={FILE_ID}",
    OUTPUT,
    quiet=False
)

model = joblib.load(OUTPUT)

# Load label encoders correctly
label_encoder = pkl.load(open("label_encoder.pkl", 'rb'))
#model=pkl.load(open("model.pkl",'rb'))


st.write("This is a web application")

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)
#-----------------------------------
#----Header---------
#----------------------------------
st.markdown("""
<h1 style='text-align:center;color:#1E3A8A;'>
📊 Customer Churn Prediction System
</h1>

<p style='text-align:center;font-size:18px;color:gray;'>
Predict whether a telecom customer is likely to churn using Machine Learning.
</p>
""", unsafe_allow_html=True)
# Input fields
# -------------------------------
# Customer Information
# -------------------------------
with st.expander("📱 Customer Information", expanded=True):

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        Partner = st.selectbox("Partner", ["No", "Yes"])
        PhoneService = st.selectbox("Phone Service", ["No", "Yes"])
        MonthlyCharges = st.number_input("Monthly Charges", 0.0, 200.0, 100.0)

    with col2:
        SeniorCitizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        Dependents = st.selectbox("Dependents", ["No", "Yes"])
        MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 2000.0)

# -------------------------------
# Internet Services
# -------------------------------
with st.expander("🌐 Internet Services", expanded=True):

    col1, col2 = st.columns(2)

    with col1:
        InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        OnlineBackup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        DeviceProtection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])

    with col2:
        TechSupport = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        StreamingTV = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

# -------------------------------
# Billing Information
# -------------------------------
with st.expander("💳 Billing Information", expanded=True):

    col1, col2 = st.columns(2)

    with col1:
        Contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        PaymentMethod = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    with col2:
        PaperlessBilling = st.selectbox(
            "Paperless Billing",
            ["No", "Yes"]
        )

        tenure_group = st.selectbox(
            "Tenure Group",
            ["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
        )



print(label_encoder['tenure_group'].classes_)
# Prediction button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Predict Churn", use_container_width=True):
    
    st.write("Input Values:")
    columns = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents','PhoneService',
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges','tenure_group'
    ]

    input_data = [
        label_encoder['gender'].transform([gender])[0],
        1 if SeniorCitizen == "Yes" else 0,
        label_encoder['Partner'].transform([Partner])[0],
        label_encoder['Dependents'].transform([Dependents])[0],
        label_encoder['PhoneService'].transform([PhoneService])[0],
        label_encoder['MultipleLines'].transform([MultipleLines])[0],
        label_encoder['InternetService'].transform([InternetService])[0],
        label_encoder['OnlineSecurity'].transform([OnlineSecurity])[0],
        label_encoder['OnlineBackup'].transform([OnlineBackup])[0],
        label_encoder['DeviceProtection'].transform([DeviceProtection])[0],
        label_encoder['TechSupport'].transform([TechSupport])[0],
        label_encoder['StreamingTV'].transform([StreamingTV])[0],
        label_encoder['StreamingMovies'].transform([StreamingMovies])[0],
        label_encoder['Contract'].transform([Contract])[0],
        label_encoder['PaperlessBilling'].transform([PaperlessBilling])[0],
        label_encoder['PaymentMethod'].transform([PaymentMethod])[0],
        MonthlyCharges,
        TotalCharges,
        label_encoder['tenure_group'].transform([tenure_group])[0]
    ]
    # Create DataFrame
    myinput = pd.DataFrame([input_data], columns=columns)
    result=model.predict(myinput)
    
    if result[0]==1:
        st.markdown("""
        <div style="background:#FEE2E2;padding:10px;
        border-radius:12px;border-left:8px solid red">
        <h3>⚠ Customer is likely to Churn</h3>
        </div>""",unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#DCFCE7;padding:10px;
        border-radius:12px;border-left:8px solid green">
        <h3>✅ Customer is NOT likely to Churn</h3>
        </div>""",unsafe_allow_html=True)

st.markdown("""

<style>
.stApp{
    background: linear-gradient(to right, #E3F2FD, #FFFFFF);


}

/* Header */
h1{
    color:#1E3A8A;
}

.stButton>button{
    background:#2563EB;
    color:white;
    border-radius:10px;
    height:55px;
    width:100%;
    font-size:20px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

div[data-baseweb="select"]{
    border-radius:10px;
}

.stNumberInput input{
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.image("logo.jpg", width=600)

    st.title("Customer Churn")

    st.info("""
    ### Features

    ✔ Machine Learning Prediction

    ✔ Telecom Dataset

    ✔ Interactive Dashboard

    ✔ Real-time Results
    """)
#---------------------------------
#---------Footer------------------
#--------------------------------
st.markdown("---")

st.markdown(
"""
<center>
Developed by <b>Snehal Kolekar</b><br>
Machine Learning Project | Streamlit | Python
</center>
""",
unsafe_allow_html=True)
