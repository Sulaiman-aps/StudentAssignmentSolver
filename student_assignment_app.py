import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Create folder for uploads
UPLOAD_FOLDER = "uploaded_assignments"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Page config
st.set_page_config(page_title="Student Assignment Submission", page_icon="📚", layout="centered")

st.title("📚 Student Assignment Submission Portal")
st.write("Please fill in your details and upload your assignment.")

# Personal Info
name = st.text_input("Full Name")
student_id = st.text_input("Student ID")
email = st.text_input("Email")
time_required = st.number_input("Time required to complete (in hours)", min_value=0.0, step=0.5)

# Language Selection
language = st.radio("Assignment Language", ["Arabic", "English"])

# File Upload
uploaded_file = st.file_uploader("Upload your assignment file", type=["pdf", "docx", "txt"])

# Submit Button
if st.button("Submit Assignment"):
    if not name or not student_id or not email or not uploaded_file:
        st.error("⚠️ Please fill all fields and upload a file.")
    else:
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Save submission details
        submission_data = {
            "Name": name,
            "Student ID": student_id,
            "Email": email,
            "Time Required (hours)": time_required,
            "Language": language,
            "File Name": uploaded_file.name,
            "Submission Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save to CSV
        csv_file = "submissions.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([submission_data])], ignore_index=True)
        else:
            df = pd.DataFrame([submission_data])
        df.to_csv(csv_file, index=False)

        st.success("✅ Assignment submitted successfully!")
        st.write("Thank you, your submission has been recorded.")

        # Show submitted data to student
        st.subheader("📄 Submission Summary")
        st.json(submission_data)
