
# Streamlit Application Specification: AI Exit-Readiness & Valuation Impact Calculator

## 1. Application Overview

This Streamlit application takes the user, **Jane Doe**, a Portfolio Manager at **Alpha Capital**, through a crucial step in preparing one of her portfolio companies, **InnovateTech**, for exit. In today's competitive market, a compelling AI narrative can significantly impact a company's valuation. Jane's mission is to systematically assess InnovateTech's AI capabilities, quantify the potential uplift in its exit multiple, and synthesize these findings into a persuasive, data-driven narrative for strategic and financial buyers.

The application guides Jane through a story-driven workflow, mirroring the realistic sequence of decisions and analyses she would perform:
1.  **Setting the Stage**: Jane identifies the company and her role.
2.  **Assessing AI Capabilities**: She evaluates InnovateTech's AI across three critical dimensions: Visible, Documented, and Sustainable.
3.  **Calculating the Readiness Score**: She configures the weighting of these dimensions to derive a comprehensive Exit-AI-R Score.
4.  **Projecting Valuation Impact**: She then uses this score to project the potential uplift in InnovateTech's EBITDA multiple.
5.  **Crafting the Narrative**: Finally, the application generates a structured report, transforming her quantitative insights into a compelling story for buyers.

The application avoids direct explanations of AI concepts, instead showing how Jane utilizes these concepts and the underlying model to make informed decisions and advance her real-world task of optimizing InnovateTech's exit strategy.

**Learning Goals for the Persona:**
By interacting with this application, Jane (and by extension, the user) will gain applied skills in:
*   **Systematic AI Assessment:** Applying a structured framework (Visible, Documented, Sustainable dimensions) to evaluate a company's AI maturity from a buyer's perspective.
*   **Quantifying AI Value:** Understanding how to calculate a weighted AI readiness score (Exit-AI-R) and translate it into a projected valuation impact.
*   **Strategic Valuation Modeling:** Adjusting key parameters like dimension weights and AI premium coefficients to explore different market scenarios and their influence on exit multiples.
*   **Data-Driven Narrative Development:** Synthesizing quantitative assessments and financial projections into a coherent and persuasive AI-centric story for potential investors and acquirers.

---

## 2. User Interface Requirements

The UI will follow a linear, sequential narrative flow, presenting each step as a distinct section on a single scrollable page. Progression will be driven by user input and explicit action buttons, ensuring the persona experiences an unfolding scenario.

#### Layout & Navigation Structure

The application will feature a clear, top-down layout with distinct sections, each introduced by a relevant narrative header. A "Reset" button in the sidebar will allow Jane to start over.

*   **Page Title:** "AI Exit-Readiness & Valuation Impact Calculator"
*   **Section 1: Setup and Introduction**
    *   Narrative context for Jane Doe and InnovateTech.
    *   Input widgets for persona and company details.
    *   Initial welcome message.
*   **Section 2: Assessing InnovateTech's AI Exit-Readiness Dimensions**
    *   Narrative explaining the three dimensions.
    *   Slider widgets for scoring each dimension.
    *   Interactive button to plot scores.
    *   Visualization of dimension scores.
*   **Section 3: Calculating the Overall Exit-AI-R Score**
    *   Narrative introducing the Exit-AI-R formula.
    *   Numeric input widgets for customizing weights.
    *   Interactive button to calculate the score.
    *   Display of the calculated Exit-AI-R Score.
*   **Section 4: Projecting Valuation Uplift through AI Premium**
    *   Narrative introducing the valuation projection formula.
    *   Numeric input for baseline multiple and slider for AI premium coefficient.
    *   Interactive button to project and plot.
    *   Display of baseline and projected multiples.
    *   Visualization of valuation comparison.
*   **Section 5: Crafting the Compelling AI Exit Narrative**
    *   Narrative emphasizing the importance of a structured report.
    *   Interactive button to generate the narrative report.
    *   Display of the comprehensive narrative report within an expander.

#### Input Widgets and Controls

All inputs will be bound to `st.session_state` for persistence.

1.  **Section 1: Setup and Introduction**
    *   **Widget:** `st.text_input`
        *   **Purpose:** To personalize the application and define the context of the assessment.
        *   **Persona Action:** Jane inputs her name, firm, and the portfolio company she is evaluating.
        *   **Parameters:**
            *   `label="Persona Name"` (Default: "Jane Doe")
            *   `label="Firm Name"` (Default: "Alpha Capital")
            *   `label="Company Name"` (Default: "InnovateTech")
2.  **Section 2: Assessing InnovateTech's AI Exit-Readiness Dimensions**
    *   **Widget:** `st.slider` (3 instances)
        *   **Purpose:** To allow Jane to subjectively rate InnovateTech's AI capabilities across key dimensions based on her knowledge and due diligence.
        *   **Persona Action:** Jane evaluates and scores each dimension, directly influencing the subsequent calculations.
        *   **Parameters:**
            *   `label="Visible AI Capabilities Score (0-100)"` (Range: 0-100, Step: 1, Default: 75)
            *   `label="Documented AI Impact Score (0-100)"` (Range: 0-100, Step: 1, Default: 60)
            *   `label="Sustainable AI Capabilities Score (0-100)"` (Range: 0-100, Step: 1, Default: 80)
    *   **Widget:** `st.button`
        *   **Purpose:** To trigger the visualization of the dimension scores after input.
        *   **Persona Action:** Jane confirms her scores and wants to see them visualized.
        *   **Parameters:** `label="Plot Dimension Scores"`
3.  **Section 3: Calculating the Overall Exit-AI-R Score**
    *   **Widget:** `st.number_input` (3 instances)
        *   **Purpose:** To allow Jane to customize the weighting of each AI dimension, reflecting varying buyer priorities or market dynamics.
        *   **Persona Action:** Jane adjusts the importance of each dimension in the overall readiness score.
        *   **Parameters:**
            *   `label="Weight for Visible AI ($w_1$)"` (Min: 0.0, Max: 1.0, Step: 0.05, Default: 0.35, Format: "%.2f")
            *   `label="Weight for Documented AI ($w_2$)"` (Min: 0.0, Max: 1.0, Step: 0.05, Default: 0.40, Format: "%.2f")
            *   `label="Weight for Sustainable AI ($w_3$)"` (Min: 0.0, Max: 1.0, Step: 0.05, Default: 0.25, Format: "%.2f")
    *   **Widget:** `st.button`
        *   **Purpose:** To trigger the calculation and display of the final Exit-AI-R score.
        *   **Persona Action:** Jane initiates the calculation to see InnovateTech's overall AI readiness.
        *   **Parameters:** `label="Calculate Exit-AI-R Score"`
4.  **Section 4: Projecting Valuation Uplift through AI Premium**
    *   **Widget:** `st.number_input`
        *   **Purpose:** To input the sector's benchmark valuation multiple.
        *   **Persona Action:** Jane provides the baseline market valuation against which InnovateTech's AI premium will be measured.
        *   **Parameters:** `label="Baseline EBITDA Multiple"` (Min: 0.0, Max: 20.0, Step: 0.1, Default: 7.0, Format: "%.1f")
    *   **Widget:** `st.slider`
        *   **Purpose:** To model the market's willingness to pay a premium for AI capabilities.
        *   **Persona Action:** Jane explores different market appetites for AI-enabled companies, assessing the sensitivity of valuation uplift.
        *   **Parameters:** `label="AI Premium Coefficient ($\delta$)"` (Min: 0.0, Max: 5.0, Step: 0.1, Default: 2.0)
    *   **Widget:** `st.button`
        *   **Purpose:** To trigger the valuation projection and its visual comparison.
        *   **Persona Action:** Jane wants to see the projected valuation impact of InnovateTech's AI.
        *   **Parameters:** `label="Project Valuation Uplift"`
5.  **Section 5: Crafting the Compelling AI Exit Narrative**
    *   **Widget:** `st.button`
        *   **Purpose:** To compile all previous inputs, scores, and projections into a comprehensive narrative report.
        *   **Persona Action:** Jane generates the final document to present to potential buyers.
        *   **Parameters:** `label="Generate AI Exit Narrative"`

#### Visualization Components

All plots will use `matplotlib` and `seaborn` with `seaborn.set_theme(style="whitegrid")` for consistent aesthetics.

1.  **Section 2: AI Exit-Readiness Dimension Scores**
    *   **Chart Type:** Bar Chart
    *   **Libraries:** `matplotlib.pyplot`, `seaborn`
    *   **Expected Output:** A bar chart showing 'Visible', 'Documented', and 'Sustainable' scores.
        *   X-axis: AI Capability Dimension (Labels: 'Visible', 'Documented', 'Sustainable')
        *   Y-axis: Score (Range: 0-100)
        *   Title: "InnovateTech's AI Exit-Readiness Dimension Scores"
        *   Purpose: Provides Jane with an immediate visual summary of InnovateTech's strengths and weaknesses in AI, highlighting areas for potential narrative emphasis or improvement.

2.  **Section 4: Valuation Multiple Comparison**
    *   **Chart Type:** Bar Chart
    *   **Libraries:** `matplotlib.pyplot`, `seaborn`
    *   **Expected Output:** A bar chart comparing the 'Baseline EBITDA Multiple' with the 'Projected EBITDA Multiple (with AI Premium)'.
        *   X-axis: Metric (Labels: 'Baseline EBITDA Multiple', 'Projected EBITDA Multiple (with AI Premium)')
        *   Y-axis: EBITDA Multiple (x)
        *   Title: "InnovateTech's Valuation Multiple Comparison"
        *   Purpose: Visually demonstrates the financial upside of InnovateTech's AI capabilities, providing a powerful talking point for Jane's exit narrative.

#### Interactive Elements & Feedback Mechanisms

*   **Weight Normalization Feedback:** After `st.button("Calculate Exit-AI-R Score")` is pressed, if the sum of weights ($w_1, w_2, w_3$) is not approximately 1.0, a warning message will appear: `st.warning(f"Warning: Provided weights sum to {total_weight:.2f}. Normalizing to 1.0 for calculation.")`. This informs Jane that the system has adjusted her input for a valid score, reinforcing the underlying mathematical rigor.
*   **Dynamic Displays:** Calculated scores and projected multiples will be displayed numerically immediately after their respective calculation buttons are pressed, ensuring Jane sees immediate results of her adjustments.
*   **Report Generation:** The final narrative report will appear within a `st.expander` to keep the main flow clean, allowing Jane to review the comprehensive output when ready.

---

## 3. Additional Requirements

#### Annotations & Tooltips

Contextual explanations will be woven into the narrative flow using `st.markdown` or `st.info` blocks, appearing near relevant input fields or outputs, helping Jane understand the significance of her actions and the resulting metrics in the context of her job.

*   **Near Dimension Sliders:**
    *   `Visible`: "Reflects how clearly buyers can perceive InnovateTech's AI in products, services, and core technology stack, indicating immediate market differentiation."
    *   `Documented`: "Quantifies the proven financial return on AI investments, such as ROI and EBITDA uplift, providing auditable evidence of value creation."
    *   `Sustainable`: "Measures the deep integration of AI capabilities, including talent, governance, and scalable processes, assuring buyers of long-term value and low integration risk."
*   **Near Weight Inputs:** "Adjust these weights to reflect how potential buyers (strategic or financial) typically prioritize Visible capabilities, Documented impact, and Sustainable foundations in AI-enabled companies."
*   **Near AI Premium Coefficient ($\delta$) Slider:** "This coefficient represents the market's enthusiasm for AI-driven value. A higher $\delta$ implies greater valuation premiums for strong AI capabilities in a given market segment."
*   **After Exit-AI-R Score:** "The **Exit-AI-R Score** quantifies InnovateTech's overall AI readiness, directly influencing the valuation premium potential. A higher score signifies a more attractive AI proposition for buyers."
*   **After Projected Multiple:** "This **Projected EBITDA Multiple** demonstrates the tangible financial benefit of InnovateTech's AI maturity, a critical figure for anchoring your exit negotiations."

#### State Management Requirements

All user inputs and calculated results will be stored and managed using `st.session_state`.
*   `st.session_state.persona_name`
*   `st.session_state.firm_name`
*   `st.session_state.company_name`
*   `st.session_state.visible_score`
*   `st.session_state.documented_score`
*   `st.session_state.sustainable_score`
*   `st.session_state.w_visible`
*   `st.session_state.w_documented`
*   `st.session_state.w_sustainable`
*   `st.session_state.exit_ai_r_score`
*   `st.session_state.baseline_ebitda_multiple`
*   `st.session_state.ai_premium_coefficient`
*   `st.session_state.projected_ebitda_multiple`

These variables will be initialized at the start of the script to default values or `None` if no default is suitable, ensuring no data loss as Jane navigates or interacts with the application.

---

## 4. Notebook Content and Code Requirements

This section maps the Jupyter Notebook content directly to Streamlit components and functionalities, ensuring all computations and narrative elements are faithfully reproduced.

```python
# Streamlit Application: AI Exit-Readiness & Valuation Impact Calculator

import streamlit as st
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


# --- Utility Functions (from notebook) ---
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
    ai_multiple_uplift = (premium_coeff * score) / 100
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
    narrative = f"""
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
"""
    return narrative

# --- Streamlit UI Layout ---
st.title("AI Exit-Readiness & Valuation Impact Calculator")

# Sidebar for Reset button
with st.sidebar:
    st.header("Control Panel")
    if st.button("Reset Application"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

## 1. Setup and Introduction
st.header("1. Setting the Stage: InnovateTech's Exit Readiness")
st.markdown(
    f"""
    As **{st.session_state.persona_name}**, a Portfolio Manager at **{st.session_state.firm_name}**,
    I am currently preparing for the exit of **{st.session_state.company_name}**, one of our key portfolio companies.
    In today's market, a strong AI narrative is crucial for attracting top-tier strategic and financial buyers and achieving a premium valuation.

    My objective is to systematically evaluate {st.session_state.company_name}'s AI capabilities from a buyer's perspective,
    quantify the potential uplift in its exit multiple, and structure a compelling AI-centric narrative.
    """
)

st.subheader("Persona & Company Details")
st.session_state.persona_name = st.text_input("Persona Name", value=st.session_state.persona_name, key="persona_name_input")
st.session_state.firm_name = st.text_input("Firm Name", value=st.session_state.firm_name, key="firm_name_input")
st.session_state.company_name = st.text_input("Company Name", value=st.session_state.company_name, key="company_name_input")

st.markdown("---")

## 2. Assessing InnovateTech's AI Exit-Readiness Dimensions
st.header("2. Assessing InnovateTech's AI Exit-Readiness Dimensions")
st.markdown(
    """
    To evaluate InnovateTech's AI value proposition for potential buyers,
    we assess its capabilities across three critical dimensions:

    *   **Visible**: How apparent are the AI capabilities? (Product features, tech stack)
    *   **Documented**: Is there proven financial impact? (ROI, EBITDA uplift)
    *   **Sustainable**: Is it deeply embedded? (Talent, governance, scalable processes)

    **Instructions:** Use the sliders below to rate InnovateTech on each dimension (0-100).
    """
)

# Sliders for dimension scores
st.session_state.visible_score = st.slider(
    "Visible AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.visible_score, step=1,
    help="Reflects how clearly buyers can perceive InnovateTech's AI in products, services, and core technology stack.",
    key="visible_score_slider"
)
st.info("🎯 *Visible*: Buyers value clear product features and a modern tech stack as signs of competitive moat.")

st.session_state.documented_score = st.slider(
    "Documented AI Impact Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.documented_score, step=1,
    help="Quantifies the proven financial return on AI investments, such as ROI and EBITDA uplift.",
    key="documented_score_slider"
)
st.info("💰 *Documented*: Quantified financial improvements prove that our AI is a profit-center, not just a cost-center.")

st.session_state.sustainable_score = st.slider(
    "Sustainable AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.sustainable_score, step=1,
    help="Measures the deep integration of AI capabilities, including talent, governance, and scalable processes.",
    key="sustainable_score_slider"
)
st.info("🌱 *Sustainable*: Embedded processes, retained talent, and a robust technology foundation assure buyers of long-term value.")

if st.button("Plot Dimension Scores", key="plot_scores_button"):
    st.session_state.plot_scores_triggered = True

if st.session_state.plot_scores_triggered:
    innovatech_scores = {
        'Visible': st.session_state.visible_score,
        'Documented': st.session_state.documented_score,
        'Sustainable': st.session_state.sustainable_score
    }
    plot_dimension_scores(innovatech_scores, st.session_state.company_name)

st.markdown("---")

## 3. Calculating the Overall Exit-AI-R Score
st.header("3. Calculating the Overall Exit-AI-R Score")
st.markdown(
    """
    The **Exit-AI-R Score** is a weighted average of the three dimensions. Buyers typically weight 'Documented' impact highest,
    followed by 'Visible' capabilities, and then 'Sustainable' foundations.

    You can adjust these weights ($w_1, w_2, w_3$) to reflect specific buyer priorities.
    The sum of the weights will be normalized to $1.0$ for the calculation.

    $$Exit\\text{-}AI\\text{-}R = w_1 \\cdot Visible + w_2 \\cdot Documented + w_3 \\cdot Sustainable$$
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.w_visible = st.number_input(
        "Weight for Visible AI ($w_1$)",
        min_value=0.0, max_value=1.0, value=st.session_state.w_visible, step=0.05, format="%.2f",
        key="w_visible_input"
    )
with col2:
    st.session_state.w_documented = st.number_input(
        "Weight for Documented AI ($w_2$)",
        min_value=0.0, max_value=1.0, value=st.session_state.w_documented, step=0.05, format="%.2f",
        key="w_documented_input"
    )
with col3:
    st.session_state.w_sustainable = st.number_input(
        "Weight for Sustainable AI ($w_3$)",
        min_value=0.0, max_value=1.0, value=st.session_state.w_sustainable, step=0.05, format="%.2f",
        key="w_sustainable_input"
    )

st.info("💡 Adjust these weights to reflect how potential buyers (strategic or financial) typically prioritize Visible capabilities, Documented impact, and Sustainable foundations in AI-enabled companies.")

if st.button("Calculate Exit-AI-R Score", key="calculate_air_button"):
    st.session_state.calculate_air_triggered = True
    st.session_state.exit_ai_r_score, _, _, _ = calculate_exit_air_score(
        st.session_state.visible_score,
        st.session_state.documented_score,
        st.session_state.sustainable_score,
        st.session_state.w_visible,
        st.session_state.w_documented,
        st.session_state.w_sustainable
    )

if st.session_state.calculate_air_triggered and st.session_state.exit_ai_r_score is not None:
    st.markdown(f"### {st.session_state.company_name}'s calculated Exit-AI-R Score is: **{st.session_state.exit_ai_r_score:.2f}**")
    st.info(f"📈 This **Exit-AI-R Score** quantifies {st.session_state.company_name}'s overall AI readiness, directly influencing the valuation premium potential. A higher score signifies a more attractive AI proposition for buyers.")

st.markdown("---")

## 4. Projecting Valuation Uplift through AI Premium
st.header("4. Projecting Valuation Uplift through AI Premium")
st.markdown(
    """
    Now, let's project the potential exit valuation by adding an **AI Premium** to the sector's baseline EBITDA multiple.
    The premium is determined by the Exit-AI-R Score and a market coefficient ($\delta$).

    $$Multiple_{projected} = Multiple_{baseline} + \\delta \\cdot \\frac{Exit\\text{-}AI\\text{-}R}{100}$$
    """
)

if st.session_state.exit_ai_r_score is None:
    st.warning("Please calculate the Exit-AI-R Score in the previous section to proceed.")
else:
    col_base, col_coeff = st.columns(2)
    with col_base:
        st.session_state.baseline_ebitda_multiple = st.number_input(
            "Baseline EBITDA Multiple",
            min_value=0.0, max_value=20.0, value=st.session_state.baseline_ebitda_multiple, step=0.1, format="%.1f",
            key="baseline_ebitda_multiple_input"
        )
    with col_coeff:
        st.session_state.ai_premium_coefficient = st.slider(
            "AI Premium Coefficient ($\delta$)",
            min_value=0.0, max_value=5.0, value=st.session_state.ai_premium_coefficient, step=0.1,
            help="This coefficient represents the market's enthusiasm for AI-driven value.",
            key="ai_premium_coefficient_slider"
        )
    st.info("📊 This coefficient reflects the market's appetite for AI-driven companies. A higher value means the market is willing to pay more for strong AI capabilities.")

    if st.button("Project Valuation Uplift", key="project_valuation_button"):
        st.session_state.project_valuation_triggered = True
        st.session_state.projected_ebitda_multiple = project_valuation_impact(
            st.session_state.exit_ai_r_score,
            st.session_state.baseline_ebitda_multiple,
            st.session_state.ai_premium_coefficient
        )

    if st.session_state.project_valuation_triggered and st.session_state.projected_ebitda_multiple is not None:
        st.markdown(f"\nBaseline EBITDA Multiple: **{st.session_state.baseline_ebitda_multiple:.2f}x**")
        st.markdown(f"Projected EBITDA Multiple (with AI Premium): **{st.session_state.projected_ebitda_multiple:.2f}x**")
        st.info(f"💰 This **Projected EBITDA Multiple** demonstrates the tangible financial benefit of {st.session_state.company_name}'s AI maturity, a critical figure for anchoring your exit negotiations.")
        plot_valuation_comparison(st.session_state.baseline_ebitda_multiple, st.session_state.projected_ebitda_multiple, st.session_state.company_name)

st.markdown("---")

## 5. Crafting the Compelling AI Exit Narrative
st.header("5. Crafting the Compelling AI Exit Narrative")
st.markdown(
    """
    The final step is to synthesize these quantitative insights into a structured narrative for the
    Information Memorandum (IM) or management presentation. This report will articulate
    InnovateTech's AI-driven value to potential buyers.
    """
)

if st.session_state.projected_ebitda_multiple is None:
    st.warning("Please complete the valuation projection in the previous section to generate the narrative report.")
else:
    if st.button("Generate AI Exit Narrative", key="generate_narrative_button"):
        st.session_state.generate_narrative_triggered = True

    if st.session_state.generate_narrative_triggered:
        narrative_text = generate_ai_exit_narrative(
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
        with st.expander("View Generated AI Exit Narrative Report"):
            st.markdown(narrative_text)
        st.info("📝 This report synthesizes all your assessments and calculations into a structured, compelling story for potential acquirers, highlighting InnovateTech's AI-driven value.")

st.markdown("---")
st.caption(f"Developed for {st.session_state.firm_name} by {st.session_state.persona_name}.")
```
