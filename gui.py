import streamlit as st
import subprocess
import os
from PIL import Image

def main():
    st.title("NFA to DFA Converter")

    # Input parameters for the nfa python file 
    param1 = st.file_uploader("Input File:", type=["json"])
    param2 = st.text_input("Output File Name:")

    # Button to execute the external script
    if st.button("Convert"):
        execute_script(param1.name, param2)
        image()

def execute_script(param1, param2):
    try:
        script_path = "main.py"

        # Run the nfa converted with venv 
        command = ["venv/bin/python", script_path, param1, param2]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

        stdout, stderr = process.communicate(input=f"{param1}\n{param2}\n")
    except Exception as e:
        st.error(f"Error executing script: {e}")


def image():
    st.title("Image Viewer")

    # store path for the image files
    image1 = "dfa.png" 
    image2 = "nfa.png" 

    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="NFA", use_column_width=True)

    with col2:
            st.image(image2, caption="DFA", use_column_width=True)

if __name__ == "__main__":
    main()

