import streamlit as st
import pandas as pd
import os
from io import BytesIO
import time

# Set page configuration
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for unique color scheme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E2F;  /* Dark blue background */
        color: #E0E0E0;            /* Light gray text */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;            /* White headings */
    }
    .stButton button {
        background-color: #4CAF50; /* Green buttons */
        color: white;
    }
    .stDownloadButton button {
        background-color: #008CBA; /* Blue download buttons */
        color: white;
    }
    .stCheckbox label {
        color: #E0E0E0;            /* Light gray checkbox labels */
    }
    .stSelectbox label {
        color: #E0E0E0;            /* Light gray selectbox labels */
    }
    .stDataFrame {
        background-color: #2E2E3F; /* Darker blue for dataframes */
        color: #E0E0E0;            /* Light gray text in dataframes */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📀DataSweeper Sterling Integrator By muqaddas ")
st.write("Transform Your File between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Directory to save submitted files
SUBMISSION_DIR = "submitted_files"
os.makedirs(SUBMISSION_DIR, exist_ok=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.write(f"🔍Preview the head of the DataFrame for {file.name}:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅Missing values have been filled!")

        # Data transformation options
        st.subheader("Data Transformation Options")
        if st.checkbox(f"Transform data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Convert {file.name} to CSV"):
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{os.path.splitext(file.name)[0]}.csv",
                        mime="text/csv",
                    )

            with col2:
                if st.button(f"Convert {file.name} to Excel"):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Sheet1')
                    st.download_button(
                        label="Download Excel",
                        data=output.getvalue(),
                        file_name=f"{os.path.splitext(file.name)[0]}.xlsx",
                        mime="application/vnd.ms-excel",
                    )

        # Data visualization options
        st.subheader("📊Data Visualization Options")
        if st.checkbox(f"Visualize data for {file.name}"):
            chart_type = st.selectbox(f"Select chart type for {file.name}", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])

            if chart_type == "Line Chart":
                st.line_chart(df)

            elif chart_type == "Bar Chart":
                st.bar_chart(df)

            elif chart_type == "Scatter Plot":
                x_axis = st.selectbox("Select X-axis", df.columns)
                y_axis = st.selectbox("Select Y-axis", df.columns)
                st.write(f"Scatter plot of {x_axis} vs {y_axis}")
                st.scatter_chart(df[[x_axis, y_axis]])

            elif chart_type == "Histogram":
                column = st.selectbox("Select column for histogram", df.columns)
                st.write(f"Histogram of {column}")
                value_counts_df = df[column].value_counts().reset_index()
                value_counts_df.columns = [column, "Count"]
                st.bar_chart(value_counts_df["Count"]) 

            elif chart_type ==" line chart ,bar chart ,scatter plot":
                st.bar_chart(value_counts_df.set_index(column))
                st.bar_chart(value_counts_df, x=column, y="count")

                

        # File submission option
        st.subheader("File Submission")
        if st.checkbox(f"Submit {file.name} for processing"):
            if st.button(f"Submit {file.name}"):
                with st.spinner(f"Submitting {file.name}..."):
                    # Simulate file submission by saving to a directory
                    submission_path = os.path.join(SUBMISSION_DIR, file.name)
                    if file_ext == ".csv":
                        df.to_csv(submission_path, index=False)
                    elif file_ext == ".xlsx":
                        df.to_excel(submission_path, index=False)
                    time.sleep(2)  # Simulate processing delay
                    st.success(f"{file.name} submitted successfully! Saved to {submission_path}")

        # Growth mindset message
        st.markdown("""
        **Growth Mindset Tip:** 
        Don't be afraid to experiment with your data! Try different cleaning and visualization techniques to uncover insights. 
        Every mistake is a learning opportunity. Keep exploring and improving!
        """)

else:
    st.write("Please upload a file to get started.")