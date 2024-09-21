import streamlit as st
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Create a mock model for demonstration
class MockModel:
    def predict(self, X):
        return np.random.choice(['Overweight', 'Normal Weight'], size=len(X))

model = MockModel()  # Replace this with your actual model

# Streamlit app layout
st.title("Weight Status Predictor")

# User inputs
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=0, max_value=120, value=25)
height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
family_history = st.selectbox("Family History of Overweight", ["Yes", "No"])
fawc = st.selectbox("FAVC (Frequent Eating Out)", ["Yes", "No"])
fcvc = st.number_input("FCVC (Frequency of Vegetables Consumption)", min_value=0, max_value=7, value=3)
ncp = st.number_input("NCP (Number of Main Meals)", min_value=1, max_value=10, value=3)
caec = st.selectbox("CAEC (Consumption of Food Between Meals)", ["Sometimes", "Always", "Never"])
smoke = st.selectbox("SMOKE (Smoking Status)", ["Yes", "No"])
ch2o = st.number_input("CH2O (Daily Water Consumption)", min_value=0, value=2)
scc = st.selectbox("SCC (Calories Consumption)", ["Yes", "No"])
faf = st.number_input("FAF (Physical Activity Frequency)", min_value=0, max_value=7, value=3)
tue = st.number_input("TUE (Time using technology)", min_value=0, value=1)
calc = st.selectbox("CALC (Consumption of Calcium)", ["Yes", "No"])
mtrans = st.selectbox("MTRANS (Transportation)", ["Walking", "Bike", "Car", "Public Transportation"])

# Prepare input for prediction
input_data = pd.DataFrame({
    'Gender': [gender],
    'Age': [age],
    'Height': [height],
    'Weight': [weight],
    'family_history_with_overweight': [family_history],
    'FAVC': [fawc],
    'FCVC': [fcvc],
    'NCP': [ncp],
    'CAEC': [caec],
    'SMOKE': [smoke],
    'CH2O': [ch2o],
    'SCC': [scc],
    'FAF': [faf],
    'TUE': [tue],
    'CALC': [calc],
    'MTRANS': [mtrans]
})

# Define your numeric and categorical attributes
num_attribs = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
cat_attribs = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

full_pipeline = ColumnTransformer([
    ('num', num_pipeline, num_attribs),
    ('cat', cat_pipeline, cat_attribs)
])

# Transform input data
input_data_prepared = full_pipeline.fit_transform(input_data)

# Make prediction
prediction = model.predict(input_data_prepared)

# Display the result
if st.button("Predict"):
    st.write(f"Predicted Weight Status: {prediction[0]}")
