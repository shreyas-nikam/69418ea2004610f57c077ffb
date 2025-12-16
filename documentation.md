id: 69418ea2004610f57c077ffb_documentation
summary: Exit-Readiness AI Narrative & Valuation Impact Calculator Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Building an AI Exit-Readiness & Valuation Impact Calculator with Streamlit

## 1. Introduction to QuLab and AI Exit-Readiness
Duration: 00:05

Welcome to the QuLab Codelab! This guide will walk you through the **QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator**, a powerful Streamlit application designed to help portfolio managers assess and articulate the AI value of their portfolio companies.

### Why is AI Exit-Readiness Critical?
In today's M&A landscape, a company's Artificial Intelligence capabilities are no longer just a feature—they are a significant driver of valuation and strategic interest. Acquiring firms are actively seeking targets with:
*   **Visible AI Assets:** Clear evidence of AI integrated into products and services.
*   **Documented AI Impact:** Quantifiable financial returns and operational efficiencies derived from AI.
*   **Sustainable AI Foundations:** Robust governance, talent, and scalable infrastructure that ensures long-term AI value.

By systematically evaluating these dimensions, we can quantify a company's AI maturity, project its impact on valuation multiples, and craft a compelling narrative for potential buyers.

### What You'll Learn
In this codelab, you will:
*   Understand the **story-driven workflow** of the application, mirroring a real-world M&A due diligence process.
*   Explore how **Streamlit** is used to create an interactive, data-driven web application.
*   Learn about **session state management** and **data caching** in Streamlit for persistence and performance.
*   Dive into the **business logic** behind calculating AI readiness scores and projecting valuation uplifts.
*   Discover how to generate a **structured AI exit narrative** based on quantitative assessments.

### Application Architecture Overview
The QuLab application follows a client-side architecture facilitated by Streamlit:
*   **User Interface (UI):** Built entirely with Streamlit components (sliders, text inputs, buttons, plots) for an interactive experience.
*   **Session State (`st.session_state`):** Crucial for maintaining user inputs and calculated results across reruns and interactions.
*   **Caching (`st.cache_data`):** Used for computationally intensive or data-loading functions (like plotting and narrative generation) to optimize performance.
*   **Business Logic:** Python functions handle calculations (weighted averages, valuation projections) and data manipulation (plotting with `pandas`, `matplotlib`, `seaborn`).

This structure allows for a fast development cycle and a highly responsive user experience without the need for a separate backend server.

<aside class="positive">
This application helps to systematically quantify the elusive value of AI, translating technological prowess into tangible financial projections and a persuasive strategic narrative, which is invaluable in the M&A process.
</aside>

## 2. Setting Up Your Environment and Running the Application
Duration: 00:10

Before we dive into the code, let's ensure you have the necessary environment set up and know how to run the application.

### Prerequisites
Make sure you have Python installed (version 3.8 or higher is recommended).

1.  **Create a virtual environment (optional but recommended):**
    ```console
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    *   On Windows:
        ```console
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```console
        source venv/bin/activate
        ```
3.  **Install Streamlit and other dependencies:**
    The application uses `streamlit`, `pandas`, `numpy`, `matplotlib`, and `seaborn`.
    ```console
    pip install streamlit pandas numpy matplotlib seaborn
    ```

### Running the Application
1.  **Save the provided Python code:** Save the application code into a file named `qu_lab_app.py` (or any `.py` name you prefer).
2.  **Run the Streamlit application:**
    ```console
    streamlit run qu_lab_app.py
    ```
    This will open the application in your default web browser, usually at `http://localhost:8501`.

### Understanding the Code Structure
Let's look at the initial setup in the application code, focusing on imports, page configuration, and session state initialization:

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore') # Suppress warnings

sns.set_theme(style="whitegrid") # Set a consistent aesthetic for plots

#  Streamlit Page Configuration 
st.set_page_config(page_title="QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator", layout="wide")

#  Sidebar 
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.sidebar.header("Control Panel")

# Reset Application button logic
if st.sidebar.button("Reset Application", key="sidebar_reset_button"):
    st.session_state.clear()
    # Re-initialize all default session state variables
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
    st.rerun() # Force a rerun to apply defaults

st.sidebar.divider()

st.title("QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator")
st.divider()

#  Initialize session state for persistent variables 
# These initializations use the "if not in" pattern, which is standard for Streamlit
# to maintain state across reruns, unless explicitly cleared (like by the reset button).
if 'persona_name' not in st.session_state:
    st.session_state.persona_name = "Jane Doe"
# ... (similar initializations for other session state variables follow)
```

<aside class="positive">
The `st.session_state` is critical for maintaining data across page reruns in Streamlit. Initializing it with `if 'key' not in st.session_state:` ensures that values persist unless explicitly cleared (e.g., by the "Reset Application" button). The `st.rerun()` call after clearing `st.session_state` forces the app to re-render with default values.
</aside>

## 3. Defining Persona and Company Details
Duration: 00:05

The first interactive step in the application allows you to define the context for your analysis: the persona (who is performing the analysis), the firm, and the target company. These details are used throughout the narrative and reports, providing a personalized and relevant context.

### UI Implementation
The application uses `st.text_input` widgets to capture these strings and stores them directly in `st.session_state` for persistence across interactions.

```python
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
```

<aside class="positive">
Using `st.session_state` as the `value` argument for input widgets ensures that the widget's current state is always reflected in the session state, and vice versa. The `key` argument is crucial for Streamlit to uniquely identify widgets, especially when they might appear conditionally or in loops.
</aside>

## 4. Assessing AI Capabilities Across Key Dimensions
Duration: 00:10

This section focuses on evaluating the target company's AI capabilities across three critical dimensions: Visible, Documented, and Sustainable. These scores form the foundation for the overall AI readiness assessment, providing a structured approach to qualitative evaluation.

### The Three Dimensions
*   **Visible AI Capabilities:** How apparent is AI in the company's products, services, and technology? (e.g., AI-powered features, intuitive UIs, public-facing data science teams). This reflects immediate market differentiation.
*   **Documented AI Impact:** What is the quantifiable proof of AI's financial or operational impact? (e.g., ROI from AI projects, EBITDA uplift, cost savings, revenue generation directly attributable to AI). This provides auditable evidence of value creation.
*   **Sustainable AI Capabilities:** How deeply integrated and future-proof are the AI capabilities? (e.g., strong AI talent pool, robust MLOps, ethical AI governance, scalable infrastructure). This assures buyers of long-term value and low integration risk.

### UI and Scoring Implementation
`st.slider` widgets are used to allow users to rate the company on each dimension from 0 to 100. An info box (`st.info`) provides context for each dimension, guiding the user's assessment.

```python
st.header("2. Assessing InnovateTech's AI Exit-Readiness Dimensions")
st.markdown(
    """
    To evaluate InnovateTech's AI value proposition for potential buyers,
    we assess its capabilities across three critical dimensions: Visible, Documented, and Sustainable.

    **Instructions:** Use the sliders below to rate InnovateTech on each dimension (0-100) based on your due diligence.
    """
)

st.session_state.visible_score = st.slider(
    "Visible AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.visible_score, step=1,
    key="visible_score_slider"
)
<aside class="positive">
🎯 <b>Visible</b>: Reflects how clearly buyers can perceive InnovateTech's AI in products, services, and core technology stack, indicating immediate market differentiation.
</aside>

st.session_state.documented_score = st.slider(
    "Documented AI Impact Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.documented_score, step=1,
    key="documented_score_slider"
)
<aside class="positive">
💰 <b>Documented</b>: Quantifies the proven financial return on AI investments, such as ROI and EBITDA uplift, providing auditable evidence of value creation.
</aside>

st.session_state.sustainable_score = st.slider(
    "Sustainable AI Capabilities Score (0-100)",
    min_value=0, max_value=100, value=st.session_state.sustainable_score, step=1,
    key="sustainable_score_slider"
)
<aside class="positive">
🌱 <b>Sustainable</b>: Measures the deep integration of AI capabilities, including talent, governance, and scalable processes, assuring buyers of long-term value and low integration risk.
</aside>

if st.button("Plot Dimension Scores", key="plot_scores_button"):
    st.session_state.plot_scores_triggered = True

if st.session_state.plot_scores_triggered:
    innovatech_scores = {
        'Visible': st.session_state.visible_score,
        'Documented': st.session_state.documented_score,
        'Sustainable': st.session_state.sustainable_score
    }
    plot_dimension_scores_cached(innovatech_scores, st.session_state.company_name)
```

### Visualizing Scores
The `plot_dimension_scores_cached` function, decorated with `@st.cache_data`, generates a bar chart using `seaborn` and `matplotlib` to visually represent the assigned scores, making it easy to grasp the company's strengths and weaknesses at a glance.

```python
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
```
<aside class="positive">
Decorating plotting functions with `@st.cache_data` (or `@st.cache_resource` for more complex objects) is a great way to optimize Streamlit applications. It prevents re-running expensive computations (like generating plots) on every rerun, as long as the inputs to the function remain the same.
</aside>

## 5. Calculating the Overall Exit-AI-R Score
Duration: 00:10

Once the individual dimension scores are set, the next step is to calculate a single, composite **Exit-AI-R Score**. This score is a weighted average, allowing you to prioritize certain dimensions based on specific market contexts or buyer profiles.

### The Exit-AI-R Formula
The Exit-AI-R Score is calculated using the following weighted average formula:

$$Exit\text{-}AI\text{-}R = w_{Visible} \cdot Visible + w_{Documented} \cdot Documented + w_{Sustainable} \cdot Sustainable$$

Where $Visible$, $Documented$, and $Sustainable$ are the scores for each dimension, and $w_{Visible}$, $w_{Documented}$, and $w_{Sustainable}$ are their respective custom weights. The application includes logic to normalize the weights if their sum is not exactly 1.0.

### Weight Customization and Calculation
`st.number_input` widgets allow users to specify the weights, and a button triggers the calculation. `st.columns` is used here for a clean side-by-side layout of the weight inputs.

```python
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

<aside class="positive">
Adjust these weights to reflect how potential buyers (strategic or financial) typically prioritize Visible capabilities, Documented impact, and Sustainable foundations in AI-enabled companies.
</aside>

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
    <aside class="positive">
📈 The <b>Exit-AI-R Score</b> quantifies {st.session_state.company_name}'s overall AI readiness, directly influencing the valuation premium potential. A higher score signifies a more attractive AI proposition for buyers.
</aside>
```

### The `calculate_exit_air_score` Function
This function includes important logic for weight normalization and robust error handling, ensuring that the calculation proceeds correctly even with imperfect user inputs.

```python
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
```
<aside class="negative">
It's crucial to handle cases where user inputs might lead to mathematical errors (e.g., weights summing to zero). The `calculate_exit_air_score` function demonstrates good practice by using `np.isclose` for float comparison and `st.warning`/`st.error` for user feedback, preventing crashes and guiding the user.
</aside>

## 6. Projecting Valuation Uplift with AI Premium
Duration: 00:15

This section allows you to translate the calculated Exit-AI-R Score into a tangible financial impact by projecting a potential uplift in the company's EBITDA multiple. This is a critical step for demonstrating AI's value to potential investors and anchoring negotiation strategies.

### The Valuation Impact Formula
The projected EBITDA multiple is calculated by adding an AI Premium to a baseline multiple:

$$Multiple_{projected} = Multiple_{baseline} + \delta \cdot \frac{Exit\text{-}AI\text{-}R}{100}$$

Where:
*   $Multiple_{projected}$ is the projected EBITDA multiple including the AI premium.
*   $Multiple_{baseline}$ is the sector's average baseline EBITDA multiple without specific AI considerations.
*   $\delta$ (delta) is the AI Premium Coefficient, representing market enthusiasm for AI-driven value.
*   $Exit\text{-}AI\text{-}R$ is the calculated Exit-AI-R Score (ranging from 0 to 100).

### UI and Projection Logic
Users can input a `Baseline EBITDA Multiple` (representing the average industry multiple) and adjust the `AI Premium Coefficient` ($\delta$) using `st.number_input` and `st.slider`. The UI is conditionally rendered, requiring the Exit-AI-R score to be calculated first.

```python
st.header("4. Projecting Valuation Uplift through AI Premium")
st.markdown(
    """
    Now, let's project the potential exit valuation by adding an **AI Premium** to the sector's baseline EBITDA multiple.
    This premium reflects the market's willingness to pay more for companies with strong, integrated AI capabilities,
    driven by InnovateTech's calculated Exit-AI-R Score and a market-specific AI Premium Coefficient ($\delta$).
    """
)
st.markdown(r"""
$$Multiple_{projected} = Multiple_{baseline} + \delta \cdot \frac{Exit\text{-}AI\text{-}R}{100}$$
""")
st.markdown(f"""
where:
- $Multiple_{{projected}}$ is the projected EBITDA multiple including the AI premium.
- $Multiple_{{baseline}}$ is the sector's average baseline EBITDA multiple without specific AI considerations.
- $\delta$ (delta) is the AI Premium Coefficient, representing market enthusiasm for AI-driven value.
- $Exit\\text{{-}}AI\\text{{-}}R$ is the calculated Exit-AI-R Score (ranging from 0 to 100).
""")

# Conditional rendering of widgets and button based on exit_ai_r_score
if st.session_state.exit_ai_r_score is None:
    <aside class="negative">
Please calculate the Exit-AI-R Score in the previous section to proceed with valuation projection.
</aside>
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
            key="ai_premium_coefficient_slider"
        )
    <aside class="positive">
📊 This coefficient represents the market's enthusiasm for AI-driven value. A higher $\delta$ implies greater valuation premiums for strong AI capabilities in a given market segment.
</aside>

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
        <aside class="positive">
💰 This <b>Projected EBITDA Multiple</b> demonstrates the tangible financial benefit of {st.session_state.company_name}'s AI maturity, a critical figure for anchoring your exit negotiations.
</aside>
        plot_valuation_comparison_cached(st.session_state.baseline_ebitda_multiple, st.session_state.projected_ebitda_multiple, st.session_state.company_name)
```
<aside class="positive">
The `AI Premium Coefficient` is a powerful lever. Adjusting it allows financial analysts to model different market conditions or buyer appetites for AI-driven companies, making the valuation projection more dynamic and realistic.
</aside>

### The `project_valuation_impact_cached` and `plot_valuation_comparison_cached` Functions

```python
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
```

## 7. Crafting the Compelling AI Exit Narrative
Duration: 00:10

The final and most crucial output of the QuLab application is a comprehensive AI exit narrative. This report synthesizes all the quantitative assessments—the individual dimension scores, the overall Exit-AI-R Score, and the projected valuation uplift—into a persuasive, structured story for potential acquirers.

### Importance of the Narrative
A well-crafted narrative is essential for:
*   **Communicating Value:** Clearly articulating how AI contributes to the company's competitive advantage and future growth.
*   **Anchoring Valuation:** Justifying the projected premium and providing data-driven arguments during negotiations.
*   **Streamlining Due Diligence:** Providing a coherent overview that highlights key strengths and reduces buyer effort.

### Narrative Generation
A single button press triggers the `generate_ai_exit_narrative_cached` function, which compiles all the data into a Markdown-formatted report, displayed using `st.expander`. The UI for this section is also conditionally rendered, dependent on the completion of the valuation projection.

```python
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
    <aside class="negative">
Please complete the valuation projection in the previous section to generate the narrative report.
</aside>
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
        <aside class="positive">
📝 This comprehensive report synthesizes all your assessments and calculations into a structured, compelling story for potential acquirers, highlighting InnovateTech's AI-driven value proposition and the tangible financial impact.
</aside>
```

### The `generate_ai_exit_narrative_cached` Function
This function dynamically creates a detailed report by pulling all relevant data from the session state. It demonstrates how to leverage f-strings and Markdown formatting to build a professional-looking document, including proper LaTeX syntax for mathematical symbols like $\delta$.

```python
@st.cache_data
def generate_ai_exit_narrative_cached(company, air_score, visible, documented, sustainable, base_mult, proj_mult, delta, persona_name, firm_name):
    """
    Generates a comprehensive AI exit narrative report.
    """
    narrative = f"""

**{company}: Quantified AI Exit Narrative Report**
Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}
Prepared by: {persona_name}, {firm_name}


**Executive Summary:**
{company} demonstrates a strong AI readiness for exit, with an overall **Exit-AI-R Score of {air_score:.2f}**.
This robust capability is projected to contribute to a significant valuation uplift, transforming the
baseline sector EBITDA multiple of {base_mult:.2f}x to an estimated **{proj_mult:.2f}x**.
This uplift, driven by an AI Premium Coefficient ($\delta$) of {delta:.2f}, underscores the market's
recognition of {company}'s advanced AI integration and value creation potential.

**1. AI Exit-Readiness Assessment Details:**
*   **Overall Exit-AI-R Score**: {air_score:.2f} (out of 100)
*   **Visible AI Capabilities Score**: {visible:.0f}/100
*   **Documented AI Impact Score**: {documented:.0f}/100
*   **Sustainable AI Capabilities Score**: {sustainable:.0f}/100

**2. Projected Valuation Impact:**
*   **Baseline Sector EBITDA Multiple**: {base_mult:.2f}x
*   **AI Premium Coefficient ($\delta$)**: {delta:.2f} turns
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


"""
    return narrative
```
<aside class="positive">
Generating rich text or reports from within Streamlit is a powerful feature. You can extend this further by offering options to download the narrative as a PDF or Word document using libraries like `reportlab` or `python-docx` for more advanced document generation capabilities.
</aside>

## 8. Advanced Streamlit Concepts and Future Enhancements
Duration: 00:10

This final step summarizes some advanced Streamlit concepts used effectively in the application and discusses potential future enhancements to extend its functionality and robustness.

### Streamlit Best Practices Highlighted
*   **`st.session_state` for Persistency:** We've seen how `st.session_state` is fundamental for building interactive Streamlit apps where data needs to persist across reruns. The "Reset Application" button in the sidebar is a prime example of controlled state management.
*   **`@st.cache_data` for Performance:** Caching expensive function calls (like plotting and narrative generation) dramatically improves the user experience by reducing load times.
*   **Conditional UI Rendering:** Using Python `if` statements to show or hide widgets, buttons, and results based on the application's state (e.g., `if st.session_state.exit_ai_r_score is None:`) ensures a logical user flow and prevents premature interaction.
*   **Layout and Information Widgets:** Effective use of `st.sidebar`, `st.columns`, `st.info`, `st.warning`, `st.expander`, and markdown allows for a well-structured and user-friendly interface that guides the user through the workflow.
*   **Mathematical Formulas:** Streamlit's robust support for LaTeX within markdown (`$...$` and `$$...$$`) makes it easy to display complex formulas clearly and professionally within the application.

### Potential Future Enhancements
1.  **More Sophisticated Scoring Models:** Integrate machine learning models that analyze company data (e.g., patent filings, annual reports, product reviews) to suggest initial scores for the AI dimensions, moving beyond manual slider inputs.
2.  **User Authentication and Profiles:** For sensitive financial data, implement user login and role-based access control, allowing multiple users to manage their own analyses.
3.  **Data Persistence for Multiple Companies:** Allow users to save and load assessments for different companies, perhaps by integrating with a database (e.g., SQLite, PostgreSQL) or cloud storage.
4.  **Sensitivity Analysis and Scenario Planning:** Add interactive plots that show how the projected valuation changes with varying AI Premium Coefficients or Exit-AI-R Scores, enabling "what-if" analyses.
5.  **Industry Benchmarking:** Include real-time or historical industry benchmark data for AI capabilities and EBITDA multiples to provide external context for the assessed scores.
6.  **Downloadable Reports:** Implement functionality to download the generated narrative as a PDF or editable document (e.g., using `reportlab` or `python-docx`).

This QuLab application serves as an excellent example of how Streamlit can be used to quickly develop powerful, data-driven tools for complex business problems like M&A strategy and valuation, transforming qualitative insights into quantitative impacts and persuasive narratives.

<aside class="positive">
You've successfully explored the QuLab application, understanding its functionalities, underlying code, and the Streamlit concepts that bring it to life. You're now equipped to build similar interactive data applications!
</aside>
