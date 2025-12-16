
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output in the console. Streamlit's own warnings are handled separately.
warnings.filterwarnings('ignore')

# Set a consistent aesthetic for plots
sns.set_theme(style="whitegrid")

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator", layout="wide")

# --- Sidebar ---
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.sidebar.header("Control Panel")

# Initialize session state fully within the sidebar reset button callback
# This ensures that when a reset occurs, all state is wiped and then re-set to defaults
# before the rerun, making the app's state consistent after a reset.
if st.sidebar.button("Reset Application", key="sidebar_reset_button"):
    st.session_state.clear()
    st.session_state.persona_name = "Jane Doe"
    st.session_state.firm_name = "Alpha Capital"
    st.session_state.company_name = "InnovateTech"
    st.session_state.visible_score = 75
    st.session_state.documented_score = 60
    st.session_state.sustainable_score = 80
    st.session_state.w_visible = 0.35
    st.session_state.w_documented = 0.40
    st.session_state.w_sustainable = 0.25
    st.session_state.exit_ai_r_score = None
    st.session_state.baseline_ebitda_multiple = 7.0
    st.session_state.ai_premium_coefficient = 2.0
    st.session_state.projected_ebitda_multiple = None
    st.session_state.plot_scores_triggered = False
    st.session_state.calculate_air_triggered = False
    st.session_state.project_valuation_triggered = False
    st.session_state.generate_narrative_triggered = False
    st.rerun()

st.sidebar.divider()

# --- Main Application Title ---
st.title("QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator")
st.divider()

# --- Initialize session state for persistent variables ---
# These initializations use the "if not in" pattern, which is standard for Streamlit
# to maintain state across reruns, unless explicitly cleared (like by the reset button).
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

# Flags to control conditional display of results/plots after button clicks
if 'plot_scores_triggered' not in st.session_state:
    st.session_state.plot_scores_triggered = False
if 'calculate_air_triggered' not in st.session_state:
    st.session_state.calculate_air_triggered = False
if 'project_valuation_triggered' not in st.session_state:
    st.session_state.project_valuation_triggered = False
if 'generate_narrative_triggered' not in st.session_state:
    st.session_state.generate_narrative_triggered = False


# --- Business Logic / Story Flow Introduction ---
st.markdown("""
As **Jane Doe**, a Portfolio Manager at **Alpha Capital**, your mission is to systematically assess one of your portfolio companies,
**InnovateTech**, for exit readiness, specifically focusing on its Artificial Intelligence capabilities.
In today's competitive market, a compelling AI narrative can significantly impact a company's valuation,
attracting top-tier strategic and financial buyers.

This application provides a structured, story-driven workflow to:

*   **Systematically Assess AI Capabilities:** Apply a structured framework (Visible, Documented, Sustainable dimensions) to evaluate InnovateTech's AI maturity from a buyer's perspective.
*   **Quantify AI Value:** Calculate a weighted AI readiness score (Exit-AI-R) and translate it into a projected valuation impact.
*   **Strategic Valuation Modeling:** Adjust key parameters like dimension weights and AI premium coefficients to explore different market scenarios and their influence on exit multiples.
*   **Data-Driven Narrative Development:** Synthesize quantitative assessments and financial projections into a coherent and persuasive AI-centric story for potential investors and acquirers.

Let's begin the journey of maximizing InnovateTech's exit value!
""")
st.markdown("---")


# --- Utility Functions ---
@st.cache_data
def plot_dimension_scores_cached(scores_dict, company_name):
    """
    Generates a bar chart visualizing the individual AI readiness dimension scores.
    This cached version handles the plotting and returns a dummy value for caching.
    """
    df_scores = pd.DataFrame(list(scores_dict.items()), columns=['Dimension', 'Score'])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Dimension', y='Score', data=df_scores, palette='viridis', ax=ax)
    ax.set_ylim(0, 100)
    ax.set_title(f"{company_name}'s AI Exit-Readiness Dimension Scores")
    ax.set_ylabel("Score (0-100)")
    ax.set_xlabel("AI Capability Dimension")
    st.pyplot(fig) # Display the plot in Streamlit
    plt.close(fig) # Close the figure to free up memory
    return True # Return a dummy value for cache_data to work

# No @st.cache_data for calculate_exit_air_score because it might interact with st.warning directly,
# and its output (a tuple including normalized weights) is simple enough not to require caching benefits.
def calculate_exit_air_score(visible, documented, sustainable, w_v, w_d, w_s):
    """
    Calculates the overall Exit-AI-R Score based on dimension scores and custom weights.
    Also handles weight normalization.
    """
    total_weight = w_v + w_d + w_s
    
    # Check if total_weight is approximately 1.0, allowing for floating point inaccuracies
    if not np.isclose(total_weight, 1.0):
        st.warning(f"Warning: Provided weights sum to {total_weight:.2f}. Normalizing to 1.0 for calculation.")
        # Ensure that normalization doesn't divide by zero if total_weight is very small or zero
        if total_weight == 0:
            st.error("Error: Sum of weights is zero, cannot normalize. Please provide valid weights.")
            return 0.0, 0.0, 0.0, 0.0 # Return default values to prevent further errors
        w_v_norm = w_v / total_weight
        w_d_norm = w_d / total_weight
        w_s_norm = w_s / total_weight
    else:
        w_v_norm = w_v
        w_d_norm = w_d
        w_s_norm = w_s

    score = (w_v_norm * visible + w_d_norm * documented + w_s_norm * sustainable)
    return score, w_v_norm, w_d_norm, w_s_norm

@st.cache_data
def project_valuation_impact_cached(score, baseline, premium_coeff):
    """
    Projects the potential valuation multiple uplift attributable to the Exit-AI-R score.
    The score is normalized by 100 as it's a percentage-like value (0-100).
    """
    ai_multiple_uplift = (premium_coeff * score) / 100
    projected = baseline + ai_multiple_uplift
    return projected

@st.cache_data
def plot_valuation_comparison_cached(baseline, projected, company_name):
    """
    Generates a bar chart comparing the baseline and projected EBITDA multiples.
    This cached version handles the plotting and returns a dummy value for caching.
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
    plt.close(fig) # Close the figure to free up memory
    return True # Return a dummy value for cache_data

@st.cache_data
def generate_ai_exit_narrative_cached(company, air_score, visible, documented, sustainable, base_mult, proj_mult, delta, persona_name, firm_name):
    """
    Generates a comprehensive AI exit narrative report.
    Fixed f-string and SyntaxWarning for LaTeX commands.
    """
    # Use double backslashes for literal backslashes in f-strings when they are part of LaTeX commands
    # (e.g., `\\delta` to produce `\delta` in Markdown).
    narrative = f"""
---
**{company}: Quantified AI Exit Narrative Report**
Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}
Prepared by: {persona_name}, {firm_name}
---

**Executive Summary:**
{company} demonstrates a strong AI readiness for exit, with an overall **Exit-AI-R Score of {air_score:.2f}**.
This robust capability is projected to contribute to a significant valuation uplift, transforming the
baseline sector EBITDA multiple of {base_mult:.2f}x to an estimated **{proj_mult:.2f}x**.
This uplift, driven by an AI Premium Coefficient ($\\delta$) of {delta:.2f}, underscores the market's
recognition of {company}'s advanced AI integration and value creation potential.

**1. AI Exit-Readiness Assessment Details:**
*   **Overall Exit-AI-R Score**: {air_score:.2f} (out of 100)
*   **Visible AI Capabilities Score**: {visible:.0f}/100
*   **Documented AI Impact Score**: {documented:.0f}/100
*   **Sustainable AI Capabilities Score**: {sustainable:.0f}/100

**2. Projected Valuation Impact:**
*   **Baseline Sector EBITDA Multiple**: {base_mult:.2f}x
*   **AI Premium Coefficient ($\\delta$)**: {delta:.2f} turns
*   **Projected EBITDA Multiple (with AI Premium)**: {proj_mult:.2f}x
*   **Implied Multiple Uplift**: {(proj_mult - base_mult):.2f}x

**3. Strategic Narrative Points:**
*   **Strong Capability Foundation**: {company} has achieved an impressive Exit-AI-R score of {air_score:.2f},
    reflecting a deliberate and strategic build-out of AI capabilities that are poised for market recognition and premium valuation.
*   **Proven Value Creation**: With a **Documented AI Impact Score of {documented:.0f}**, {company}
    provides auditable evidence of financial return on AI investments, proving that our AI is a profit-center,
    not just a cost-center. This directly translates into higher, quantifiable value for acquirers.
*   **Market Differentiation & Visibility**: A high **Visible AI Capabilities Score of {visible:.0f}**
    ensures that potential buyers can clearly perceive and understand how InnovateTech's AI differentiates
    its products and services, creating a defensible competitive moat and immediate market appeal.
*   **Long-term & Scalable Impact**: The **Sustainable AI Capabilities Score of {sustainable:.0f}**
    assures buyers of deep integration, robust governance, a strong talent base, and scalable processes.
    This signifies low integration risk and guarantees enduring AI-driven value post-acquisition,
    making {company} a highly attractive long-term investment.

---
"""
    return narrative


# --- Streamlit UI Layout ---

## 1. Setup and Introduction
st.header("1. Setting the Stage: InnovateTech's Exit Readiness")
st.markdown(
    f"""
    As **{st.session_state.persona_name}**, a Portfolio Manager at **{st.session_state.firm_name}**,
    you are preparing for the exit of **{st.session_state.company_name}**, one of your key portfolio companies.
    Your objective is to systematically evaluate {st.session_state.company_name}'s AI capabilities from a buyer's perspective,
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
    we assess its capabilities across three critical dimensions: Visible, Documented, and Sustainable.

    **Instructions:** Use the sliders below to rate InnovateTech on each dimension (0-100) based on your due diligence.
    """
)

# Sliders for dimension scores
st.session_state.visible_score = st.slider(
    "Visible AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.visible_score, step=1,
    key="visible_score_slider"
)
st.info("🎯 **Visible**: Reflects how clearly buyers can perceive InnovateTech's AI in products, services, and core technology stack, indicating immediate market differentiation.")

st.session_state.documented_score = st.slider(
    "Documented AI Impact Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.documented_score, step=1,
    key="documented_score_slider"
)
st.info("💰 **Documented**: Quantifies the proven financial return on AI investments, such as ROI and EBITDA uplift, providing auditable evidence of value creation.")

st.session_state.sustainable_score = st.slider(
    "Sustainable AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.sustainable_score, step=1,
    key="sustainable_score_slider"
)
st.info("🌱 **Sustainable**: Measures the deep integration of AI capabilities, including talent, governance, and scalable processes, assuring buyers of long-term value and low integration risk.")

if st.button("Plot Dimension Scores", key="plot_scores_button"):
    st.session_state.plot_scores_triggered = True

if st.session_state.plot_scores_triggered:
    innovatech_scores = {
        'Visible': st.session_state.visible_score,
        'Documented': st.session_state.documented_score,
        'Sustainable': st.session_state.sustainable_score
    }
    plot_dimension_scores_cached(innovatech_scores, st.session_state.company_name)


st.markdown("---")

## 3. Calculating the Overall Exit-AI-R Score
st.header("3. Calculating the Overall Exit-AI-R Score")
st.markdown(
    """
    The **Exit-AI-R Score** is a weighted average of the three dimensions, designed to provide a comprehensive
    measure of InnovateTech's AI readiness for an exit. You can customize the weighting of each AI dimension
    to reflect varying buyer priorities or market dynamics.
    """
)
st.markdown(r"""
$$Exit\text{-}AI\text{-}R = w_1 \cdot Visible + w_2 \cdot Documented + w_3 \cdot Sustainable$$
""")
st.markdown(f"""
where:
- $Visible$ is the Visible AI Capabilities Score
- $Documented$ is the Documented AI Impact Score
- $Sustainable$ is the Sustainable AI Capabilities Score
- $w_1$, $w_2$, $w_3$ are the custom weights for each dimension.
""")

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
    st.info(f"📈 The **Exit-AI-R Score** quantifies {st.session_state.company_name}'s overall AI readiness, directly influencing the valuation premium potential. A higher score signifies a more attractive AI proposition for buyers.")

st.markdown("---")

## 4. Projecting Valuation Uplift through AI Premium
st.header("4. Projecting Valuation Uplift through AI Premium")
st.markdown(
    """
    Now, let's project the potential exit valuation by adding an **AI Premium** to the sector's baseline EBITDA multiple.
    This premium reflects the market's willingness to pay more for companies with strong, integrated AI capabilities,
    driven by InnovateTech's calculated Exit-AI-R Score and a market-specific AI Premium Coefficient ($\\delta$).
    """
)
st.markdown(r"""
$$Multiple_{projected} = Multiple_{baseline} + \delta \cdot \frac{Exit\text{-}AI\text{-}R}{100}$$
""")
# Corrected f-string for LaTeX command escapes
st.markdown(f"""
where:
- $Multiple_{{projected}}$ is the projected EBITDA multiple including the AI premium.
- $Multiple_{{baseline}}$ is the sector's average baseline EBITDA multiple without specific AI considerations.
- $\\delta$ (delta) is the AI Premium Coefficient, representing market enthusiasm for AI-driven value.
- $Exit\\text{{-}}AI\\text{{-}}R$ is the calculated Exit-AI-R Score (ranging from 0 to 100).
""")

# Conditional rendering of widgets and button based on exit_ai_r_score
if st.session_state.exit_ai_r_score is None:
    st.warning("Please calculate the Exit-AI-R Score in the previous section to proceed with valuation projection.")
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
            "AI Premium Coefficient ($\\delta$)", # Fixed \delta escape for f-string
            min_value=0.0, max_value=5.0, value=st.session_state.ai_premium_coefficient, step=0.1,
            key="ai_premium_coefficient_slider"
        )
    # Fixed \delta escape for f-string
    st.info("📊 This coefficient represents the market's enthusiasm for AI-driven value. A higher $\\delta$ implies greater valuation premiums for strong AI capabilities in a given market segment.")

    if st.button("Project Valuation Uplift", key="project_valuation_button"):
        st.session_state.project_valuation_triggered = True
        st.session_state.projected_ebitda_multiple = project_valuation_impact_cached(
            st.session_state.exit_ai_r_score,
            st.session_state.baseline_ebitda_multiple,
            st.session_state.ai_premium_coefficient
        )

    if st.session_state.project_valuation_triggered and st.session_state.projected_ebitda_multiple is not None:
        st.markdown(f"\n- Baseline EBITDA Multiple: **{st.session_state.baseline_ebitda_multiple:.2f}x**")
        st.markdown(f"- Projected EBITDA Multiple (with AI Premium): **{st.session_state.projected_ebitda_multiple:.2f}x**")
        st.info(f"💰 This **Projected EBITDA Multiple** demonstrates the tangible financial benefit of {st.session_state.company_name}'s AI maturity, a critical figure for anchoring your exit negotiations.")
        plot_valuation_comparison_cached(st.session_state.baseline_ebitda_multiple, st.session_state.projected_ebitda_multiple, st.session_state.company_name)


st.markdown("---")

## 5. Crafting the Compelling AI Exit Narrative
st.header("5. Crafting the Compelling AI Exit Narrative")
st.markdown(
    """
    The final and most crucial step is to synthesize all your quantitative insights—the AI readiness scores,
    dimension analyses, and valuation projections—into a cohesive and persuasive narrative report.
    This report will serve as a foundational document for the Information Memorandum (IM) or management presentation,
    articulating InnovateTech's unique AI-driven value proposition to potential strategic and financial buyers.
    """
)

# Conditional rendering of button based on projected_ebitda_multiple
if st.session_state.projected_ebitda_multiple is None:
    st.warning("Please complete the valuation projection in the previous section to generate the narrative report.")
else:
    if st.button("Generate AI Exit Narrative", key="generate_narrative_button"):
        st.session_state.generate_narrative_triggered = True

    if st.session_state.generate_narrative_triggered:
        narrative_text = generate_ai_exit_narrative_cached(
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
        st.info("📝 This comprehensive report synthesizes all your assessments and calculations into a structured, compelling story for potential acquirers, highlighting InnovateTech's AI-driven value proposition and the tangible financial impact.")

st.markdown("---")
st.caption(f"Developed for {st.session_state.firm_name} by {st.session_state.persona_name}.")

