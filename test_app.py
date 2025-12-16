
import pytest
import os
from streamlit.testing.v1 import AppTest
import pandas as pd
import numpy as np
import io

# Helper to create temporary files for AppTest
# In a real test setup, you'd manage these files using pytest fixtures or similar
# For this example, we'll simulate the file creation as per the prompt.

def write_file_to_github(filepath, content):
    """
    Creates a dummy file with the given content.
    Used to simulate the file structure provided in the problem description.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)

# --- Simulate file creation based on the problem description ---
# These are necessary for AppTest.from_file to find the app and its dependencies
write_file_to_github("requirements.txt", """streamlit
pandas
numpy
matplotlib
seaborn
""")

write_file_to_github("utils.py", """import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set a consistent aesthetic for plots
sns.set_theme(style="whitegrid")

# --- Initialize session state for persistent variables ---
# These are initialized once on script load/rerun or after a st.session_state.clear()
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
    st.session_state.exit_ai_r_score = None
if 'baseline_ebitda_multiple' not in st.session_state:
    st.session_state.baseline_ebitda_multiple = 7.0
if 'ai_premium_coefficient' not in st.session_state:
    st.session_state.ai_premium_coefficient = 2.0
if 'projected_ebitda_multiple' not in st.session_state:
    st.session_state.projected_ebitda_multiple = None
if 'plot_scores_triggered' not in st.session_state:
    st.session_state.plot_scores_triggered = False
if 'calculate_air_triggered' not in st.session_state:
    st.session_state.calculate_air_triggered = False
if 'project_valuation_triggered' not in st.session_state:
    st.session_state.project_valuation_triggered = False
if 'generate_narrative_triggered' not in st.session_state:
    st.session_state.generate_narrative_triggered = False


# --- Utility Functions ---
def plot_dimension_scores(scores_dict, company_name):
    """
    Generates a bar chart visualizing the individual AI readiness dimension scores.
    """
    df_scores = pd.DataFrame(list(scores_dict.items()), columns=['Dimension', 'Score'])
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Dimension', y='Score', data=df_scores, palette='viridis', ax=ax)
    ax.set_ylim(0, 100)
    ax.set_title(f"{company_name}'s AI Exit-Readiness Dimension Scores")
    ax.set_ylabel("Score (0-100)")
    ax.set_xlabel("AI Capability Dimension")
    st.pyplot(fig) # Display the plot in Streamlit
    plt.close(fig)

def calculate_exit_air_score(visible, documented, sustainable, w_v, w_d, w_s):
    """
    Calculates the overall Exit-AI-R Score based on dimension scores and custom weights.
    Also handles weight normalization.
    """
    total_weight = w_v + w_d + w_s
    if not np.isclose(total_weight, 1.0):
        st.warning(f"Warning: Provided weights sum to {total_weight:.2f}. Normalizing to 1.0 for calculation.")
        w_v_norm = w_v / total_weight
        w_d_norm = w_d / total_weight
        w_s_norm = w_s / total_weight
    else:
        w_v_norm = w_v
        w_d_norm = w_d
        w_s_norm = w_s

    score = (w_v_norm * visible + w_d_norm * documented + w_s_norm * sustainable)
    return score, w_v_norm, w_d_norm, w_s_norm

def project_valuation_impact(score, baseline, premium_coeff):
    """
    Projects the potential valuation multiple uplift attributable to the Exit-AI-R score.
    """
    # Normalize score from 0-100 to 0-1 for calculation with coefficient
    normalized_score = score / 100 
    ai_multiple_uplift = premium_coeff * normalized_score
    projected = baseline + ai_multiple_uplift
    return projected

def plot_valuation_comparison(baseline, projected, company_name):
    """
    Generates a bar chart comparing the baseline and projected EBITDA multiples.
    """
    multiples_df = pd.DataFrame({
        'Metric': ['Baseline EBITDA Multiple', 'Projected EBITDA Multiple (with AI Premium)'],
        'Value': [baseline, projected]
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Metric', y='Value', data=multiples_df, palette='coolwarm', ax=ax)
    ax.set_title(f"{company_name}'s Valuation Multiple Comparison")
    ax.set_ylabel("EBITDA Multiple (x)")
    ax.set_xlabel("")
    st.pyplot(fig) # Display the plot in Streamlit
    plt.close(fig)

def generate_ai_exit_narrative(company, air_score, visible, documented, sustainable, base_mult, proj_mult, delta, persona_name, firm_name):
    """
    Generates a comprehensive AI exit narrative report.
    """
    narrative = f\"\"\"
---
**{company}: Quantified AI Exit Narrative Report**
Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}
Prepared by: {persona_name}, {firm_name}
---

**Executive Summary:**
{company} demonstrates a strong AI readiness for exit, with an overall **Exit-AI-R Score of {air_score:.2f}**. This robust capability is projected to contribute to a significant valuation uplift, transforming the baseline sector EBITDA multiple of {base_mult:.2f}x to an estimated **{proj_mult:.2f}x**.

**1. AI Exit-Readiness Assessment Details:**
*   **Overall Exit-AI-R Score**: {air_score:.2f}
*   **Visible AI Capabilities**: {visible:.2f}/100
*   **Documented AI Impact**: {documented:.2f}/100
*   **Sustainable AI Capabilities**: {sustainable:.2f}/100

**2. Projected Valuation Impact:**
*   **Baseline Sector EBITDA Multiple**: {base_mult:.2f}x
*   **AI Premium Coefficient ($\delta$)**: {delta:.2f} turns
*   **Implied Multiple Uplift**: {(proj_mult - base_mult):.2f}x

**3. Strategic Narrative Points:**
*   **Capability Journey**: {company} has achieved an Exit-AI-R score of {air_score:.2f}, reflecting a deliberate build-out of capabilities.
*   **Value Created**: Documented financial improvements (Score: {documented:.2f}) prove that our AI is a profit-center, not just a cost-center.
*   **Competitive Position**: High visibility (Score: {visible:.2f}) in our product stack ensures a defensible moat against non-AI peers.
*   **Sustainability**: A sustainability score of {sustainable:.2f} assures buyers of low integration risk and enduring value.
---
\"\"\"
    return narrative
""")

write_file_to_github("app.py", """import streamlit as st
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
""")

write_file_to_github("application_pages/page_1_setup.py", """import streamlit as st
import utils # Access session state and utility functions

def main():
    st.header("1. Setting the Stage: InnovateTech's Exit Readiness")
    st.markdown(
        f\"\"\"
        As **{st.session_state.persona_name}**, a Portfolio Manager at **{st.session_state.firm_name}**,
        my task is to prepare **{st.session_state.company_name}** for a successful exit. In the current market,
        showcasing strong AI capabilities is a key differentiator that can significantly enhance a company's valuation.

        My goal is to thoroughly assess {st.session_state.company_name}'s AI, quantify its impact on valuation,
        and build a persuasive, data-driven narrative for potential strategic and financial buyers.
        This initial step confirms the context of our analysis.
        \"\"\"
    )

    st.subheader("Persona & Company Details")
    # Widgets update session state directly
    st.session_state.persona_name = st.text_input(
        "Persona Name",
        value=st.session_state.persona_name,
        key="persona_name_input_p1" # Ensure unique key across app
    )
    st.session_state.firm_name = st.text_input(
        "Firm Name",
        value=st.session_state.firm_name,
        key="firm_name_input_p1"
    )
    st.session_state.company_name = st.text_input(
        "Company Name",
        value=st.session_state.company_name,
        key="company_name_input_p1"
    )

    st.markdown("---")
    st.markdown(f"**Current Focus:** Assessing AI capabilities for {st.session_state.company_name}.")
""")

write_file_to_github("application_pages/page_2_assess_dimensions.py", """import streamlit as st
import utils # Access session state and utility functions

def main():
    st.header("2. Assessing InnovateTech's AI Exit-Readiness Dimensions")
    st.markdown(
        f\"\"\"
        To effectively communicate **{st.session_state.company_name}**'s AI value to buyers,
        I need to evaluate its capabilities from their perspective. Buyers look for AI that is
        not just innovative, but also tangibly impactful and resilient.

        This section helps me systematically score {st.session_state.company_name}'s AI across three critical dimensions:

        *   **Visible AI Capabilities**: How clearly can buyers see our AI in action?
        *   **Documented AI Impact**: What proven financial results has our AI delivered?
        *   **Sustainable AI Capabilities**: How well-integrated and future-proof are our AI operations?

        My subjective assessment here, informed by due diligence, will directly feed into the overall AI readiness score.
        \"\"\"
    )

    st.subheader(f"Rate {st.session_state.company_name}'s AI Capabilities (0-100)")

    # Sliders for dimension scores
    st.session_state.visible_score = st.slider(
        "Visible AI Capabilities Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.visible_score, step=1,
        key="visible_score_slider_p2"
    )
    st.info("🎯 *Visible*: This reflects how clearly buyers can perceive InnovateTech's AI in products, services, and core technology stack. A high score here indicates immediate market differentiation.")

    st.session_state.documented_score = st.slider(
        "Documented AI Impact Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.documented_score, step=1,
        key="documented_score_slider_p2"
    )
    st.info("💰 *Documented*: This quantifies the proven financial return on AI investments, such as ROI and EBITDA uplift. Providing auditable evidence of value creation is key for buyers.")

    st.session_state.sustainable_score = st.slider(
        "Sustainable AI Capabilities Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.sustainable_score, step=1,
        key="sustainable_score_slider_p2"
    )
    st.info("🌱 *Sustainable*: This measures the deep integration of AI capabilities, including talent, governance, and scalable processes. It assures buyers of long-term value and low integration risk post-acquisition.")

    st.markdown("---")

    # Button to plot scores
    if st.button("Plot Dimension Scores", key="plot_scores_button_p2"):
        st.session_state.plot_scores_triggered = True

    if st.session_state.plot_scores_triggered:
        st.markdown(f"### Visualizing {st.session_state.company_name}'s AI Strengths")
        st.markdown(
            f\"\"\"
            This chart visually summarizes {st.session_state.company_name}'s AI capabilities across the three critical dimensions.
            As a Portfolio Manager, I use this visualization to quickly grasp where InnovateTech excels
            and where there might be areas to strengthen the narrative or even implement quick wins before an exit.
            It helps me highlight key selling points to potential buyers.
            \"\"\"
        )
        innovatech_scores = {
            'Visible': st.session_state.visible_score,
            'Documented': st.session_state.documented_score,
            'Sustainable': st.session_state.sustainable_score
        }
        utils.plot_dimension_scores(innovatech_scores, st.session_state.company_name)

    st.markdown("---")
""")

write_file_to_github("application_pages/page_3_calculate_score.py", """import streamlit as st
import utils # Access session state and utility functions

def main():
    st.header("3. Calculating the Overall Exit-AI-R Score")
    st.markdown(
        f\"\"\"
        Now that I've assessed **{st.session_state.company_name}**'s AI capabilities across the individual dimensions,
        it's time to synthesize these into a single, comprehensive **Exit-AI-R Score**. This score will be a key metric
        in our exit strategy, quantifying InnovateTech's overall AI readiness.

        Buyers often prioritize different aspects of AI. For instance, a strategic buyer might heavily value
        visible capabilities, while a financial buyer might focus more on documented impact. I can reflect these
        nuances by adjusting the weights ($w_1, w_2, w_3$) for each dimension. The formula for the Exit-AI-R Score is:
        \"\"\"
    )

    st.markdown(
        r"$$Exit\\text{-}AI\\text{-}R = w_1 \\cdot Visible + w_2 \\cdot Documented + w_3 \\cdot Sustainable$$"
    )

    st.subheader("Customize Dimension Weights")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.w_visible = st.number_input(
            "Weight for Visible AI ($w_1$)",
            min_value=0.0, max_value=1.0, value=st.session_state.w_visible, step=0.05, format="%.2f",
            key="w_visible_input_p3"
        )
    with col2:
        st.session_state.w_documented = st.number_input(
            "Weight for Documented AI ($w_2$)",
            min_value=0.0, max_value=1.0, value=st.session_state.w_documented, step=0.05, format="%.2f",
            key="w_documented_input_p3"
        )
    with col3:
        st.session_state.w_sustainable = st.number_input(
            "Weight for Sustainable AI ($w_3$)",
            min_value=0.0, max_value=1.0, value=st.session_state.w_sustainable, step=0.05, format="%.2f",
            key="w_sustainable_input_p3"
        )

    st.info("💡 *Buyer Priorities*: Adjust these weights to reflect how potential buyers (strategic or financial) typically prioritize Visible capabilities, Documented impact, and Sustainable foundations in AI-enabled companies.")

    if st.button("Calculate Exit-AI-R Score", key="calculate_air_button_p3"):
        st.session_state.calculate_air_triggered = True
        st.session_state.exit_ai_r_score, _, _, _ = utils.calculate_exit_air_score(
            st.session_state.visible_score,
            st.session_state.documented_score,
            st.session_state.sustainable_score,
            st.session_state.w_visible,
            st.session_state.w_documented,
            st.session_state.w_sustainable
        )

    if st.session_state.calculate_air_triggered and st.session_state.exit_ai_r_score is not None:
        st.markdown(f"### **{st.session_state.company_name}**'s calculated Exit-AI-R Score is: **{st.session_state.exit_ai_r_score:.2f}**")
        st.info(f"📈 The **Exit-AI-R Score** quantifies {st.session_state.company_name}'s overall AI readiness, directly influencing the valuation premium potential. A higher score signifies a more attractive AI proposition for buyers.")

    st.markdown("---")
""")

write_file_to_github("application_pages/page_4_project_valuation.py", """import streamlit as st
import utils # Access session state and utility functions

def main():
    st.header("4. Projecting Valuation Uplift through AI Premium")
    st.markdown(
        f\"\"\"
        With **{st.session_state.company_name}**'s Exit-AI-R Score now calculated, I can move to the crucial step of
        projecting its potential valuation uplift. A strong AI foundation doesn't just make a company more attractive;
        it can command a tangible premium in the market.

        This section allows me to model this financial impact by considering a baseline EBITDA multiple
        for the sector and applying an **AI Premium** based on the Exit-AI-R Score. This projection provides a data-driven
        argument for a higher valuation during exit negotiations.
        \"\"\"
    )

    st.markdown(
        r"$$Multiple_{projected} = Multiple_{baseline} + \\delta \\cdot \\frac{Exit\\text{-}AI\\text{-}R}{100}$$"
    )

    if st.session_state.exit_ai_r_score is None:
        st.warning("Please navigate to '3. Calculate Exit-AI-R Score' and calculate the score to proceed with valuation projection.")
    else:
        st.subheader("Configure Valuation Parameters")
        col_base, col_coeff = st.columns(2)
        with col_base:
            st.session_state.baseline_ebitda_multiple = st.number_input(
                "Baseline EBITDA Multiple",
                min_value=0.0, max_value=20.0, value=st.session_state.baseline_ebitda_multiple, step=0.1, format="%.1f",
                key="baseline_ebitda_multiple_input_p4"
            )
        with col_coeff:
            st.session_state.ai_premium_coefficient = st.slider(
                "AI Premium Coefficient ($\delta$)",
                min_value=0.0, max_value=5.0, value=st.session_state.ai_premium_coefficient, step=0.1,
                key="ai_premium_coefficient_slider_p4"
            )
        st.info("📊 *Market Appetite*: This coefficient represents the market's enthusiasm for AI-driven value. A higher $\delta$ implies greater valuation premiums for strong AI capabilities in a given market segment.")

        if st.button("Project Valuation Uplift", key="project_valuation_button_p4"):
            st.session_state.project_valuation_triggered = True
            st.session_state.projected_ebitda_multiple = utils.project_valuation_impact(
                st.session_state.exit_ai_r_score,
                st.session_state.baseline_ebitda_multiple,
                st.session_state.ai_premium_coefficient
            )

        if st.session_state.project_valuation_triggered and st.session_state.projected_ebitda_multiple is not None:
            st.markdown(f"### **{st.session_state.company_name}**'s Valuation Projection")
            st.markdown(f"Baseline EBITDA Multiple: **{st.session_state.baseline_ebitda_multiple:.2f}x**")
            st.markdown(f"Projected EBITDA Multiple (with AI Premium): **{st.session_state.projected_ebitda_multiple:.2f}x**")
            st.info(f"💰 This **Projected EBITDA Multiple** demonstrates the tangible financial benefit of {st.session_state.company_name}'s AI maturity, a critical figure for anchoring your exit negotiations. It's a powerful narrative element!")
            utils.plot_valuation_comparison(st.session_state.baseline_ebitda_multiple, st.session_state.projected_ebitda_multiple, st.session_state.company_name)

    st.markdown("---")
""")

write_file_to_github("application_pages/page_5_craft_narrative.py", """import streamlit as st
import utils # Access session state and utility functions

def main():
    st.header("5. Crafting the Compelling AI Exit Narrative")
    st.markdown(
        f\"\"\"
        I've assessed **{st.session_state.company_name}**'s AI capabilities and quantified its potential valuation uplift.
        The final and crucial step is to consolidate these insights into a powerful, data-driven narrative.
        This narrative is not just a summary; it's a strategic communication tool that will be integrated into the
        Information Memorandum (IM) or management presentation to effectively articulate InnovateTech's AI-driven value
        to potential buyers.

        A well-structured narrative bridges the gap between technical AI prowess and tangible business value,
        making InnovateTech a more attractive acquisition target.
        \"\"\"
    )

    if st.session_state.projected_ebitda_multiple is None:
        st.warning("Please navigate to '4. Project Valuation Uplift' and complete the projection to generate the narrative report.")
    else:
        if st.button("Generate AI Exit Narrative", key="generate_narrative_button_p5"):
            st.session_state.generate_narrative_triggered = True

        if st.session_state.generate_narrative_triggered:
            narrative_text = utils.generate_ai_exit_narrative(
                st.session_state.company_name,
                st.session_state.exit_ai_r_score,
                st.session_state.visible_score,
                st.session_state.documented_score,
                st.session_state.sustainable_score,
                st.session_state.baseline_ebitda_multiple,
                st.session_state.projected_ebitda_multiple,
                st.session_state.ai_premium_coefficient,
                st.session_state.persona_name,
                st.session_state.firm_name
            )
            with st.expander("View Generated AI Exit Narrative Report", expanded=True):
                st.markdown(narrative_text)
            st.info("📝 This report synthesizes all your assessments and calculations into a structured, compelling story for potential acquirers, highlighting InnovateTech's AI-driven value. It's now ready for refinement and integration into the broader exit materials.")

    st.markdown("---")
    st.caption(f"Developed for {st.session_state.firm_name} by {st.session_state.persona_name}.")
""")
# --- End of file creation simulation ---


def test_initial_app_load_and_default_state():
    at = AppTest.from_file("app.py").run()

    # Assert initial markdown content
    assert at.markdown[0].value.startswith("In this lab, **Jane Doe**, a Portfolio Manager at **Alpha Capital**")
    assert at.markdown[0].value.strip().endswith("impact InnovateTech's exit strategy and valuation.")

    # Assert initial session state values (from utils.py defaults)
    assert at.session_state["persona_name"] == "Jane Doe"
    assert at.session_state["firm_name"] == "Alpha Capital"
    assert at.session_state["company_name"] == "InnovateTech"
    assert at.session_state["visible_score"] == 75
    assert at.session_state["documented_score"] == 60
    assert at.session_state["sustainable_score"] == 80
    assert at.session_state["w_visible"] == 0.35
    assert at.session_state["w_documented"] == 0.40
    assert at.session_state["w_sustainable"] == 0.25
    assert at.session_state["exit_ai_r_score"] is None
    assert at.session_state["baseline_ebitda_multiple"] == 7.0
    assert at.session_state["ai_premium_coefficient"] == 2.0
    assert at.session_state["projected_ebitda_multiple"] is None
    assert not at.session_state["plot_scores_triggered"]
    assert not at.session_state["calculate_air_triggered"]
    assert not at.session_state["project_valuation_triggered"]
    assert not at.session_state["generate_narrative_triggered"]

    # Assert navigation options in sidebar
    assert len(at.sidebar.selectbox) == 1
    assert at.sidebar.selectbox[0].options == [
        "1. Setup and Introduction",
        "2. Assess AI Dimensions",
        "3. Calculate Exit-AI-R Score",
        "4. Project Valuation Uplift",
        "5. Craft AI Exit Narrative"
    ]
    assert at.sidebar.selectbox[0].value == "1. Setup and Introduction"


def test_page_1_setup_interactions():
    at = AppTest.from_file("app.py").run()

    # Verify initial page 1 content
    assert "1. Setting the Stage: InnovateTech's Exit Readiness" in at.header[0].value
    assert "As **Jane Doe**, a Portfolio Manager at **Alpha Capital**, my task is to prepare **InnovateTech**" in at.markdown[1].value

    # Interact with text inputs
    at.text_input[0].set_value("John Smith").run()
    at.text_input[1].set_value("Global Investments").run()
    at.text_input[2].set_value("FutureCorp").run()

    # Assert session state updated
    assert at.session_state["persona_name"] == "John Smith"
    assert at.session_state["firm_name"] == "Global Investments"
    assert at.session_state["company_name"] == "FutureCorp"

    # Assert displayed markdown updated
    assert "As **John Smith**, a Portfolio Manager at **Global Investments**, my task is to prepare **FutureCorp**" in at.markdown[1].value
    assert "**Current Focus:** Assessing AI capabilities for FutureCorp." in at.markdown[-1].value


def test_page_2_assess_dimensions_and_plot():
    at = AppTest.from_file("app.py").run()

    # Navigate to "2. Assess AI Dimensions"
    at.sidebar.selectbox[0].set_value("2. Assess AI Dimensions").run()

    # Verify page 2 header
    assert "2. Assessing InnovateTech's AI Exit-Readiness Dimensions" in at.header[0].value

    # Change slider values
    at.slider[0].set_value(90).run()  # Visible
    at.slider[1].set_value(70).run()  # Documented
    at.slider[2].set_value(85).run()  # Sustainable

    # Assert session state updated
    assert at.session_state["visible_score"] == 90
    assert at.session_state["documented_score"] == 70
    assert at.session_state["sustainable_score"] == 85

    # Click "Plot Dimension Scores" button
    at.button[0].click().run()

    # Assert plot_scores_triggered in session state
    assert at.session_state["plot_scores_triggered"] is True

    # Assert that a matplotlib plot was generated
    assert len(at.pyplot) == 1
    assert at.pyplot[0].figure is not None
    # Can further assert plot titles or labels if needed
    # For now, just checking existence is sufficient.


def test_page_3_calculate_air_score():
    at = AppTest.from_file("app.py").run()

    # Set prerequisite session state values (scores from Page 2)
    at.session_state["visible_score"] = 90
    at.session_state["documented_score"] = 70
    at.session_state["sustainable_score"] = 85
    at.run() # Rerun to apply session state changes before navigating

    # Navigate to "3. Calculate Exit-AI-R Score"
    at.sidebar.selectbox[0].set_value("3. Calculate Exit-AI-R Score").run()

    # Verify page 3 header
    assert "3. Calculating the Overall Exit-AI-R Score" in at.header[0].value

    # Change weights (default sum to 1.0, so this should just update)
    at.number_input[0].set_value(0.40).run() # w_visible
    at.number_input[1].set_value(0.30).run() # w_documented
    at.number_input[2].set_value(0.30).run() # w_sustainable (now sum to 1.0)

    # Assert session state updated for weights
    assert at.session_state["w_visible"] == 0.40
    assert at.session_state["w_documented"] == 0.30
    assert at.session_state["w_sustainable"] == 0.30

    # Click "Calculate Exit-AI-R Score"
    at.button[0].click().run()

    # Assert calculate_air_triggered in session state
    assert at.session_state["calculate_air_triggered"] is True

    # Expected score with new weights: (0.40*90) + (0.30*70) + (0.30*85) = 36 + 21 + 25.5 = 82.5
    expected_score = 82.5
    assert abs(at.session_state["exit_ai_r_score"] - expected_score) < 0.001

    # Assert displayed score
    assert f"InnovateTech's calculated Exit-AI-R Score is: **{expected_score:.2f}**" in at.markdown[3].value
    assert len(at.info) == 1 # Check for the info box

    # Test weight normalization warning
    at.number_input[0].set_value(0.50).run() # w_visible
    at.number_input[1].set_value(0.20).run() # w_documented
    at.number_input[2].set_value(0.20).run() # w_sustainable (sum to 0.90)
    at.button[0].click().run() # Recalculate

    assert at.warning[0].value.startswith("Warning: Provided weights sum to 0.90. Normalizing to 1.0 for calculation.")
    # Expected score with normalized weights:
    # 0.5/0.9 * 90 + 0.2/0.9 * 70 + 0.2/0.9 * 85 = 50 + 15.555 + 18.888 = 84.444
    expected_score_normalized = (0.5/0.9 * 90) + (0.2/0.9 * 70) + (0.2/0.9 * 85)
    assert abs(at.session_state["exit_ai_r_score"] - expected_score_normalized) < 0.001


def test_page_4_project_valuation():
    at = AppTest.from_file("app.py").run()

    # Set prerequisite session state values (scores from Page 2 and Page 3)
    at.session_state["visible_score"] = 90
    at.session_state["documented_score"] = 70
    at.session_state["sustainable_score"] = 85
    at.session_state["w_visible"] = 0.40
    at.session_state["w_documented"] = 0.30
    at.session_state["w_sustainable"] = 0.30
    at.session_state["exit_ai_r_score"] = 82.5 # Calculated from previous test
    at.run()

    # Navigate to "4. Project Valuation Uplift"
    at.sidebar.selectbox[0].set_value("4. Project Valuation Uplift").run()

    # Verify page 4 header
    assert "4. Projecting Valuation Uplift through AI Premium" in at.header[0].value

    # Change valuation parameters
    at.number_input[0].set_value(8.0).run() # Baseline EBITDA Multiple
    at.slider[0].set_value(2.5).run()       # AI Premium Coefficient

    # Assert session state updated
    assert at.session_state["baseline_ebitda_multiple"] == 8.0
    assert at.session_state["ai_premium_coefficient"] == 2.5

    # Click "Project Valuation Uplift"
    at.button[0].click().run()

    # Assert project_valuation_triggered in session state
    assert at.session_state["project_valuation_triggered"] is True

    # Expected projected multiple: 8.0 + (2.5 * 82.5/100) = 8.0 + (2.5 * 0.825) = 8.0 + 2.0625 = 10.0625
    expected_projected_multiple = 10.0625
    assert abs(at.session_state["projected_ebitda_multiple"] - expected_projected_multiple) < 0.001

    # Assert displayed projected multiple and info box
    assert f"Baseline EBITDA Multiple: **8.00x**" in at.markdown[3].value
    assert f"Projected EBITDA Multiple (with AI Premium): **{expected_projected_multiple:.2f}x**" in at.markdown[4].value
    assert len(at.info) == 1

    # Assert that a matplotlib plot was generated
    assert len(at.pyplot) == 1
    assert at.pyplot[0].figure is not None
    # For now, just checking existence is sufficient.

    # Test warning when exit_ai_r_score is None
    at_warn = AppTest.from_file("app.py").run()
    at_warn.sidebar.selectbox[0].set_value("4. Project Valuation Uplift").run()
    assert "Please navigate to '3. Calculate Exit-AI-R Score' and calculate the score to proceed with valuation projection." in at_warn.warning[0].value


def test_page_5_craft_narrative():
    at = AppTest.from_file("app.py").run()

    # Set all prerequisite session state values to mimic a full run-through
    at.session_state["persona_name"] = "John Smith"
    at.session_state["firm_name"] = "Global Investments"
    at.session_state["company_name"] = "FutureCorp"
    at.session_state["visible_score"] = 90
    at.session_state["documented_score"] = 70
    at.session_state["sustainable_score"] = 85
    at.session_state["w_visible"] = 0.40
    at.session_state["w_documented"] = 0.30
    at.session_state["w_sustainable"] = 0.30
    at.session_state["exit_ai_r_score"] = 82.5
    at.session_state["baseline_ebitda_multiple"] = 8.0
    at.session_state["ai_premium_coefficient"] = 2.5
    at.session_state["projected_ebitda_multiple"] = 10.06
    at.run()

    # Navigate to "5. Craft AI Exit Narrative"
    at.sidebar.selectbox[0].set_value("5. Craft AI Exit Narrative").run()

    # Verify page 5 header
    assert "5. Crafting the Compelling AI Exit Narrative" in at.header[0].value

    # Click "Generate AI Exit Narrative"
    at.button[0].click().run()

    # Assert generate_narrative_triggered in session state
    assert at.session_state["generate_narrative_triggered"] is True

    # Assert the expander and its content
    assert len(at.expander) == 1
    assert at.expander[0].label == "View Generated AI Exit Narrative Report"
    assert at.expander[0].expanded is True

    narrative_content = at.expander[0].markdown[0].value
    assert "FutureCorp: Quantified AI Exit Narrative Report" in narrative_content
    assert "Prepared by: John Smith, Global Investments" in narrative_content
    assert "Exit-AI-R Score of 82.50" in narrative_content
    assert "baseline sector EBITDA multiple of 8.00x to an estimated **10.06x**." in narrative_content
    assert "Visible AI Capabilities: 90.00/100" in narrative_content
    assert "AI Premium Coefficient ($\delta$): 2.50 turns" in narrative_content
    assert "Implied Multiple Uplift: 2.06x" in narrative_content # 10.06 - 8.00

    assert len(at.info) == 1 # Check for the info box

    # Test warning when projected_ebitda_multiple is None
    at_warn = AppTest.from_file("app.py").run()
    at_warn.sidebar.selectbox[0].set_value("5. Craft AI Exit Narrative").run()
    assert "Please navigate to '4. Project Valuation Uplift' and complete the projection to generate the narrative report." in at_warn.warning[0].value


def test_reset_button():
    at = AppTest.from_file("app.py").run()

    # Change some session state values
    at.text_input[0].set_value("Test Persona").run()
    at.session_state["visible_score"] = 10
    at.session_state["exit_ai_r_score"] = 50.0
    at.session_state["plot_scores_triggered"] = True
    at.run() # Rerun to apply changes

    assert at.session_state["persona_name"] == "Test Persona"
    assert at.session_state["visible_score"] == 10
    assert at.session_state["exit_ai_r_score"] == 50.0
    assert at.session_state["plot_scores_triggered"] is True

    # Click the Reset Application button in the sidebar
    # The reset button is the first button in the sidebar
    at.sidebar.button[0].click().run()

    # Assert that session state values reverted to defaults
    assert at.session_state["persona_name"] == "Jane Doe"
    assert at.session_state["firm_name"] == "Alpha Capital"
    assert at.session_state["company_name"] == "InnovateTech"
    assert at.session_state["visible_score"] == 75 # Back to default
    assert at.session_state["documented_score"] == 60 # Back to default
    assert at.session_state["sustainable_score"] == 80 # Back to default
    assert at.session_state["exit_ai_r_score"] is None
    assert at.session_state["projected_ebitda_multiple"] is None
    assert not at.session_state["plot_scores_triggered"] # Back to default false

    # Assert that the app is back on the "1. Setup and Introduction" page
    assert at.sidebar.selectbox[0].value == "1. Setup and Introduction"
    assert "1. Setting the Stage: InnovateTech's Exit Readiness" in at.header[0].value
