
import sys
import os

# Add the directory where this script resides to the Python path
# This helps ensure that local modules like 'utils' can be imported correctly,
# especially in certain execution environments or when running from a different working directory.
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

import streamlit as st
import utils # Import utils to initialize session state and access common functions

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AI Exit-Readiness & Valuation Impact Calculator")
st.divider()

st.markdown("""
In this lab, **Jane Doe**, a Portfolio Manager at **Alpha Capital**, navigates the critical process of preparing one of her portfolio companies, **InnovateTech**, for a successful exit. Recognizing that a compelling AI narrative is a significant value driver in today's M&A landscape, Jane uses this application to:

1.  **Systematically Assess InnovateTech's AI Capabilities**: Evaluate the company's AI across key dimensions: Visible, Documented, and Sustainable.
2.  **Quantify AI Readiness**: Calculate a comprehensive Exit-AI-R Score by weighting these dimensions according to market priorities.
3.  **Project Valuation Uplift**: Model the potential impact of this AI readiness on InnovateTech's EBITDA multiple.
4.  **Craft a Data-Driven Narrative**: Generate a persuasive report for strategic and financial buyers, leveraging her quantitative analysis.

This application guides Jane through an end-to-end scenario, demonstrating how she applies AI concepts and analytical tools to make informed decisions that directly impact InnovateTech's exit strategy and valuation.
""")

# Sidebar for Reset button - placed in app.py as it affects the entire app state
with st.sidebar:
    st.header("Control Panel")
    if st.button("Reset Application"):
        st.session_state.clear()
        st.rerun()

st.sidebar.divider()

page = st.sidebar.selectbox(
    label="Navigation",
    options=[
        "1. Setup and Introduction",
        "2. Assess AI Dimensions",
        "3. Calculate Exit-AI-R Score",
        "4. Project Valuation Uplift",
        "5. Craft AI Exit Narrative"
    ]
)

# Navigation logic to call the main function of each page
if page == "1. Setup and Introduction":
    from application_pages.page_1_setup import main
    main()
elif page == "2. Assess AI Dimensions":
    from application_pages.page_2_assess_dimensions import main
    main()
elif page == "3. Calculate Exit-AI-R Score":
    from application_pages.page_3_calculate_score import main
    main()
elif page == "4. Project Valuation Uplift":
    from application_pages.page_4_project_valuation import main
    main()
elif page == "5. Craft AI Exit Narrative":
    from application_pages.page_5_craft_narrative import main
    main()

st.markdown("---")
st.caption("This application helps portfolio managers quantify and articulate the value of AI in portfolio companies for exit strategies.")
