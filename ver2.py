import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Step 1: Load the accident data from Excel
# Load the construction safety accident data from Excel
a=pd.read_excel(r'C:\Users\USER\OneDrive\바탕 화면\23-1학기\app\국토안전관리원_건설안전사고사례_20221118.xlsx')
fn=a.dropna()
data = fn


# Step 2: Clean and preprocess the data
# TODO: Implement text preprocessing techniques

# Step 3: Split the data into training and testing sets
train_data = data.sample(frac=0.8, random_state=42)
test_data = data.drop(train_data.index)

# Step 4: Train a classification model
vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_data['구체적사고원인'])
clf = MultinomialNB()
clf.fit(train_features, train_data['사고원인(주원인)'])

# Step 5: Evaluate the performance of the model
test_features = vectorizer.transform(test_data['작업프로세스'])
score = clf.score(test_features, test_data['사고원인(주원인)'])
st.write(f"Model accuracy: {score:.2f}")

# Step 6: Create a Streamlit web application
st.title("Safety Accident Prediction")

process_steps = st.text_input("Today's Process Steps:")
if st.button("Predict Accident"):
    # Step 7: Use the trained model to predict the possible safety accident
    input_features = vectorizer.transform(['작업프로세스'])
    prediction = clf.predict(input_features)[0]

    # Step 8: Display the predicted accident and provide suggestions for preventive measures
    st.write(f"Possible Accident: {prediction}")
    # TODO: Provide preventive measures based on predicted accident

    # Step 9: Show the most frequent accident types based on the input process steps
    freq_accidents = train_data[train_data['작업프로세스'].str.contains(process_steps)]['구체적사고원인'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(freq_accidents.index, freq_accidents.values)
    ax.set_xticklabels(freq_accidents.index, rotation=90)
    ax.set_ylabel('Frequency')
    ax.set_title('Most Frequent Accidents Based on Input Process Steps')
    st.pyplot(fig)
