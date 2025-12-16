
import streamlit as st
import sys
import os

# Set Streamlit page configuration
st.set_page_config(page_title="AI Exit-Readiness & Valuation Impact Calculator", layout="wide")

# Sidebar elements
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()

# --- Initialize session state for persistent variables ---
# These initializations ensure all variables exist from the start of the application
# and maintain their values across page changes or reruns.
if 'persona_name' not in st.session_state:
    st.session_state.persona_name = "Jane Doe"
if 'firm_name' not in st.session_state:
    st.session_state.firm_name = "Alpha Capital"
if 'company_name' not in st.session_state:
    st.session_state.company_name = "InnovateTech"
if 'visible_score' not in st.session_state:
    st.session_state.visible_score = 75
if 'documented_score' not in st.session_state:
    st.session_state.documented_score = 60
if 'sustainable_score' not in st.session_state:
    st.session_state.sustainable_score = 80
if 'w_visible' not in st.session_state:
    st.session_state.w_visible = 0.35
if 'w_documented' not in st.session_state:
    st.session_state.w_documented = 0.40
if 'w_sustainable' not in st.session_state:
    st.session_state.w_sustainable = 0.25
if 'exit_ai_r_score' not in st.session_state:
    st.session_state.exit_ai_r_score = None # Will be calculated
if 'baseline_ebitda_multiple' not in st.session_state:
    st.session_state.baseline_ebitda_multiple = 7.0
if 'ai_premium_coefficient' not in st.session_state:
    st.session_state.ai_premium_coefficient = 2.0
if 'projected_ebitda_multiple' not in st.session_state:
    st.session_state.projected_ebitda_multiple = None # Will be calculated

# Flags to control conditional display of results/plots after button clicks,
# ensuring outputs only appear after explicit user actions.
if 'plot_scores_triggered' not in st.session_state:
    st.session_state.plot_scores_triggered = False
if 'calculate_air_triggered' not in st.session_state:
    st.session_state.calculate_air_triggered = False
if 'project_valuation_triggered' not in st.session_state:
    st.session_state.project_valuation_triggered = False
if 'generate_narrative_triggered' not in st.session_state:
    st.session_state.generate_narrative_triggered = False

# Overall application introduction and persona's problem statement
st.markdown("""
In this lab, **Jane Doe**, a Portfolio Manager at **Alpha Capital**, embarks on a critical task: preparing her portfolio company, **InnovateTech**, for a successful exit. In today's dynamic market, the story around a company's Artificial Intelligence capabilities can profoundly influence its valuation and attractiveness to potential acquirers.

This application provides Jane with a structured, step-by-step workflow to:
1.  **Define Context**: Identify the key players and the company under assessment.
2.  **Assess AI Dimensions**: Evaluate InnovateTech's AI across crucial "Visible", "Documented", and "Sustainable" dimensions.
3.  **Quantify Readiness**: Calculate a comprehensive **Exit-AI-R Score** based on customized weightings.
4.  **Project Valuation**: Translate this readiness score into a tangible impact on the company's EBITDA multiple.
5.  **Articulate the Narrative**: Generate a data-driven report to present a compelling AI story to strategic and financial buyers.

Through this journey, Jane will learn to systematically assess, quantify, and articulate the value of AI in a real-world M&A scenario, ensuring InnovateTech achieves its optimal exit valuation.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    label="Go to Section",
    options=[
        "1. Setup and Introduction",
        "2. Assessing AI Dimensions",
        "3. Calculating Exit-AI-R Score",
        "4. Projecting Valuation Uplift",
        "5. Crafting the Exit Narrative"
    ]
)

# Reset button in the sidebar to clear all session state and restart the application
if st.sidebar.button("Reset Application"):
    st.session_state.clear()
    st.rerun()

# Page routing based on sidebar selection.
# Imports are now explicit from the 'application_pages' package.
if page == "1. Setup and Introduction":
    from application_pages.page_1_setup import main
    main()
elif page == "2. Assessing AI Dimensions":
    from application_pages.page_2_assessment import main
    main()
elif page == "3. Calculating Exit-AI-R Score":
    from application_pages.page_3_calculate_air import main
    main()
elif page == "4. Projecting Valuation Uplift":
    from application_pages.page_4_valuation import main
    main()
elif page == "5. Crafting the Exit Narrative":
    from application_pages.page_5_narrative import main
    main()


# License
st.caption('''
---
## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
''')
