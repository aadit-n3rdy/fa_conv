import streamlit as st
import subprocess
import os
from PIL import Image

def main():
    st.title("NFA to DFA Converter")

    # Input parameters for the external script
    param1 = st.text_input("Input File Name:")
    param2 = st.text_input("Output File Name:")

    # Button to execute the external script
    if st.button("Convert"):
        execute_script(param1, param2)
        image()

def execute_script(param1, param2):
    try:
        # Replace 'external_script.py' with the actual name of your Python script
        script_path = "main.py"

        # Run the external script with input parameters
        command = ["venv/bin/python", script_path, param1, param2]

        # Use subprocess.PIPE to capture the output of the external script
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

        # Communicate with the script and pass input parameters
        stdout, stderr = process.communicate(input=f"{param1}\n{param2}\n")

        # Display the output of the external script
        st.text(f"Script Output:\n{stdout}")
        st.text(f"Script Error (if any):\n{stderr}")

    except Exception as e:
        st.error(f"Error executing script: {e}")


def image():
    st.title("Image Viewer")

    # Read the image files
    image1 = "dfa.png" 
    image2 = "nfa.png" 

    # Display the images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="NFA", use_column_width=True)

    with col2:
            st.image(image2, caption="DFA", use_column_width=True)

if __name__ == "__main__":
    main()

