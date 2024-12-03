import streamlit as st
import datetime
from PIL import Image
from utils import save_issue_ticket, classify_waste, classify_issue

def add_custom_styles():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            transition: 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #45a049;
            transform: scale(1.05);
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }

        .stButton > button:active {
            transform: scale(1);
            background-color: #3e8e41;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def citizen_interface():
    add_custom_styles()  # Add styles

    st.title("Citizen Page")
    st.header("Raise an Issue Ticket")

    # Get user details
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")  # Capture user's email
    issue_description = st.text_area("Describe the Issue")
    issue_category = st.selectbox(
        "Issue Category", ["Water Management", "Garbage Collection", "Road Management", "Other"]
    )

    # Optional image upload
    uploaded_image = st.file_uploader("Upload an Image (optional)", type=["jpg", "jpeg", "png"])
    processed_image = None
    if uploaded_image:
        try:
            processed_image = Image.open(uploaded_image)
        except Exception as e:
            st.error(f"Error loading image: {e}")

    # Manual Location Input (Street, City, Pincode)
    st.subheader("Location Details")
    street = st.text_input("Street")
    city = st.text_input("City")
    pincode = st.text_input("Pincode")

    # Display the entered location
    if street and city and pincode:
        st.write(f"Street: {street}, City: {city}, Pincode: {pincode}")
    else:
        st.warning("Please enter complete address details.")

    # Submit issue
    if st.button("Submit Issue"):
        suggested_category = classify_issue(issue_description)
        waste_category = classify_waste(processed_image) if processed_image else "Not Specified"

        issue_data = {
            "name": user_name,
            "email": user_email,
            "description": issue_description,
            "category": issue_category,
            "suggested_category": suggested_category,
            "geo_location": {"street": street, "city": city, "pincode": pincode},
            "date": datetime.datetime.now().isoformat(),  # Save date in ISO format
            "status": "Open",  # Add status
        }

        save_issue_ticket(issue_data)
        st.success("Issue ticket submitted successfully!")
