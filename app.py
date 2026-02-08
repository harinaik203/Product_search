import streamlit as st
import markdown

from agent_builder import ProductAgent
from exception import CustomException


# Page configuration
st.set_page_config(
    page_title="Product Search Agent",
    layout="centered"
)

st.title("🛒 Product Search Agent")
st.caption("AI-powered product price comparison using Gemini")

# Input field
query = st.text_input("Enter your product name:")

# Search button
if st.button("Search"):
    try:
        if not query.strip():
            st.warning("Please enter a product name")
        else:
            with st.spinner("Searching the web and verifying prices..."):
                product_agent = ProductAgent()
                agent_response = product_agent.perform_task(query)

                # Convert markdown content to HTML
                response_html = markdown.markdown(
                    str(agent_response.content)
                )

                st.markdown(response_html, unsafe_allow_html=True)

    except Exception as e:
        st.error("Something went wrong while processing your request.")
        raise CustomException(e)
