import streamlit as st
import pandas as pd
import os
from io import BytesIO

# setup our app

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.write("Welcome to Data Sweeper! This app will help you clean your data in a few simple steps.Transform your data betwwen CSV, Excel, and JSON formats. Remove duplicates, missing values, and more. Let's get started!")

uploaded_file = st.file_uploader("Upload a file (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_extension}")
            continue

# Display Info About The File 

        st.write(f"File Name: {file.name}")
        st.write(f"File Type: {file_extension}")
        st.write(f"File Size: {file.size/1024}")

#show 5 rows of the dataframes

        st.write("Data Preview")
        st.dataframe(df.head())

#options to clean the data
        st.subheader("Data Cleaning Options")
    if st.checkbox(f"Clean data for {file.name}"):
       col1 ,col2 = st.columns(2)
    
       with col1:
        if st.button(f"Remove Duplicates from {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("Duplicates Removed")
    
       with col2:
        if st.button(f"Fill Missing Values for {file.name}"):
            numeric_cols = df.select_dtypes(include=["number"]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Missing Values Filled")
    
    #choose specific columns to convert
    st.subheader("Convert Data")
    columns = st.multiselect("Select Columns to Convert", df.columns ,default=df.columns)
    df = df[columns]

    #create some vizualization
    st.subheader("📊 Data Visualization")
    if st.checkbox("Show Visualization for {file.name}"):
       st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    #Convert the file Csv to Excel

    st.subheader("📀 Convert Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_extension, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_extension, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        #download the file
        st.download_button(
            label=f"🔸 Click here to download {file_name}",
            data=buffer,
            file_name=file_name,
            mime=mime_type,
        )

st.success = "Data Cleaning and Conversion Completed Successfully! 🎉"