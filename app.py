import streamlit as st
import markdown

from agent_builder import ProductAgent

st.set_page_config(
    page_title="Product Search Agent",
    layout="centered"
)

st.title("🛒 Product Search Agent")
st.caption("AI-powered product price insights")

query = st.text_input("Enter your product name:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a product name.")
    else:
        try:
            with st.spinner("Generating price insights..."):
                agent = ProductAgent()
                response = agent.perform_task(query)

                html_output = markdown.markdown(str(response.content))
                st.markdown(html_output, unsafe_allow_html=True)

        except Exception:
            # DO NOT re-raise exceptions in Streamlit
            st.error("Something went wrong while processing your request. Please try again.")
