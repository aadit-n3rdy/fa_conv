import streamlit as st
from PIL import Image

def main():
    st.title("Dual Image Viewer")

    if True:
        # Read the image files
        image1 = "images/nfa.png" 
        image2 = "images/dfa.png" 

        # Display the images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(image1, caption="Image 1", use_column_width=True)

        with col2:
            st.image(image2, caption="Image 2", use_column_width=True)

if __name__ == "__main__":
    main()

