import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pickle

model = pickle.load(open('LR Model.pkl', 'rb'))

st.set_page_config(page_title="Medical Insurance Cost Forecast", page_icon="⚕️")

# Function to load Lottie animation from URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

col1, col2 = st.columns([1,4])
with col1:
    lottie_url = "https://lottie.host/5af1d12f-7aaf-4e75-9eb0-2fe1473f43a3/zQNNZr5Ga9.json"
    lottie_json = load_lottieurl(lottie_url)
    app_icon = st_lottie(lottie_json, speed=1, width=100, height=100, key="lottie")
with col2:
    welcome_container = st.empty()
    welcome_container.header("Medical Insurance Cost Forecast")

# Define variables
age = 0
sex = ''
bmi = 0.0
children = 0
smoker = ''
region = ''

# Function to check if mandatory fields are filled
def check_mandatory_fields_filled():
    return all([age, sex, bmi, smoker, region])

# Main section for other input fields
st.subheader("Personal Information")
# Sidebar for age, sex, and BMI
col1, col2 = st.columns([2, 2])
with col1:
    age = st.number_input('Age', min_value=0, value=0)
    bmi = st.number_input("BMI (Body Mass Index)", value=0.0)
    children = st.number_input("Number of Children", min_value=0, value=0)
with col2:
    sex_display = ('Female', 'Male')
    sex = st.selectbox("Sex", sex_display)
    smoker_display = ('No', 'Yes')
    smoker = st.selectbox("Smoker", smoker_display)
    region_display = ('Northeast', 'Northwest', 'Southeast', 'Southwest')
    region = st.selectbox("Region", region_display)

# Submit button to make predictions
if st.button("Submit"):
    # Check if mandatory fields are filled
    if not check_mandatory_fields_filled():
        st.warning('Please fill in all mandatory fields to proceed.')
        st.stop()

    features = [[age, sex_display.index(sex), bmi, children, smoker_display.index(smoker), region_display.index(region)]]

    prediction = model.predict(features)

    st.success(f"Predicted Medical Insurance Cost is:  ${prediction[0]:.2f} ")
