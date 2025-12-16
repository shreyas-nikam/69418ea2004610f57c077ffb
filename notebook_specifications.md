
# Jupyter Notebook Specification: AI Exit-Readiness & Valuation Impact Calculator

## 1. Setup and Introduction

### Markdown Cell — Story + Context + Real-World Relevance

As Jane Doe, a Portfolio Manager at Alpha Capital, I am currently preparing for the exit of InnovateTech, one of our key portfolio companies. In today's market, a strong AI narrative is crucial for attracting top-tier strategic and financial buyers and achieving a premium valuation. My objective is to systematically evaluate InnovateTech's AI capabilities from a buyer's perspective, quantify the potential uplift in its exit multiple, and structure a compelling AI-centric narrative. This process will ensure that the significant value created through InnovateTech's AI initiatives is clearly articulated and financially auditable, justifying a higher valuation during the exit process.

This notebook will guide me through:
1.  **Assessing InnovateTech's AI Exit-Readiness Dimensions**: Evaluating how apparent, documented, and sustainable InnovateTech's AI capabilities are.
2.  **Calculating the Overall Exit-AI-R Score**: Combining these dimensions into a single, comprehensive score.
3.  **Projecting Valuation Uplift**: Quantifying how the Exit-AI-R score translates into a higher EBITDA multiple.
4.  **Crafting the Compelling AI Exit Narrative**: Structuring the narrative elements to effectively communicate AI value to potential buyers.

### Code cell (function definition + function execution)

```python
# 1. Install required libraries
!pip install pandas numpy matplotlib seaborn

# 2. Import required dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner notebook output
warnings.filterwarnings('ignore')

# Set a consistent aesthetic for plots
sns.set_theme(style="whitegrid")

# Define persona and company details for narrative generation
persona_name = "Jane Doe"
firm_name = "Alpha Capital"
company_name = "InnovateTech"

print(f"Welcome, {persona_name} from {firm_name}!")
print(f"Let's assess {company_name}'s AI exit readiness and its valuation impact.")
```

---

## 2. Assessing InnovateTech's AI Exit-Readiness Dimensions

### Markdown Cell — Story + Context + Real-World Relevance

As a Portfolio Manager, my first step is to thoroughly assess InnovateTech's AI capabilities across three critical dimensions that strategic and financial buyers prioritize during due diligence. These dimensions, drawn from robust industry frameworks, allow us to categorize and score InnovateTech's AI maturity:

*   **Visible**: How apparent are InnovateTech's AI capabilities to a buyer? This includes product features, technology stack, and demonstrable integrations. A high 'Visible' score creates a powerful first impression and signals tangible innovation.
*   **Documented**: Has InnovateTech quantifiably proven the impact of its AI initiatives? This dimension assesses the existence of an audit trail showing ROI, EBITDA improvements, or revenue uplift directly attributable to AI. Buyers need concrete evidence of value creation.
*   **Sustainable**: Are InnovateTech's AI capabilities deeply embedded and future-proof, or are they one-off projects reliant on a few key individuals? This covers talent, governance, processes, and a scalable technology foundation. Sustainability ensures ongoing value and reduces integration risk for an acquirer.

These scores, ranging from 0 to 100, are typically derived from detailed due diligence assessments, including management interviews and technical audits, as outlined in the comprehensive PE Org-AI-R framework.

### Code cell (function definition + function execution)

```python
def get_dimension_scores():
    """
    Prompts the user to input scores for Visible, Documented, and Sustainable AI capabilities.
    Scores should be between 0 and 100.
    """
    print("\nPlease enter InnovateTech's AI capability scores (0-100) based on your assessment:")

    while True:
        try:
            visible = float(input("Visible AI Capabilities (e.g., product features, tech stack): "))
            if not (0 <= visible <= 100):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

    while True:
        try:
            documented = float(input("Documented AI Impact (e.g., ROI, EBITDA improvements with audit trail): "))
            if not (0 <= documented <= 100):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

    while True:
        try:
            sustainable = float(input("Sustainable AI Capabilities (e.g., talent, governance, processes): "))
            if not (0 <= sustainable <= 100):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

    return {'Visible': visible, 'Documented': documented, 'Sustainable': sustainable}

def plot_dimension_scores(scores_dict):
    """
    Generates a bar chart visualizing the individual AI readiness dimension scores.
    """
    df_scores = pd.DataFrame(list(scores_dict.items()), columns=['Dimension', 'Score'])

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Dimension', y='Score', data=df_scores, palette='viridis')
    plt.ylim(0, 100)
    plt.title(f"{company_name}'s AI Exit-Readiness Dimension Scores")
    plt.ylabel("Score (0-100)")
    plt.xlabel("AI Capability Dimension")
    plt.show()

# Execution: Get user input for scores
innovatech_scores = get_dimension_scores()

# Execution: Plot the dimension scores
plot_dimension_scores(innovatech_scores)
```

### Markdown cell (explanation of execution <only if necessary>)

This visualization helps me quickly grasp InnovateTech's strengths and weaknesses across the three key AI dimensions. For example, if 'Visible' is high, I know we have strong product differentiation. If 'Documented' is lower, it signals a need to gather more quantitative evidence of AI's financial impact before buyer presentations. This clarity is crucial for tailoring our pre-exit preparations.

---

## 3. Calculating the Overall Exit-AI-R Score

### Markdown Cell — Story + Context + Real-World Relevance

Now that I have the individual dimension scores, I need to compute a single, holistic Exit-AI-R Score. This score provides a quantitative summary of InnovateTech's overall AI readiness for an exit, which can be directly linked to valuation premiums. The framework uses a weighted average to reflect the different priorities buyers place on each dimension:

*   **Documented (0.40 weight)**: Buyers heavily prioritize proven, auditable financial impact.
*   **Visible (0.35 weight)**: Strong product features and a clear tech stack make a compelling first impression.
*   **Sustainable (0.25 weight)**: Embedded capabilities reduce risk and ensure long-term value, but are harder to verify initially.

The formula for the Exit-AI-R Score is:

$$Exit-AI-R = w_1 \cdot Visible + w_2 \cdot Documented + w_3 \cdot Sustainable$$

Where:
- $w_1$ is the weight for Visible AI capabilities.
- $w_2$ is the weight for Documented AI impact.
- $w_3$ is the weight for Sustainable AI capabilities.

### Code cell (function definition + function execution)

```python
def calculate_exit_air_score(visible_score, documented_score, sustainable_score,
                             w_visible=0.35, w_documented=0.40, w_sustainable=0.25):
    """
    Calculates the overall Exit-AI-R Score based on dimension scores and custom weights.

    Args:
        visible_score (float): Score for Visible AI Capabilities (0-100).
        documented_score (float): Score for Documented AI Impact (0-100).
        sustainable_score (float): Score for Sustainable AI Capabilities (0-100).
        w_visible (float): Weight for Visible dimension. Default is 0.35.
        w_documented (float): Weight for Documented dimension. Default is 0.40.
        w_sustainable (float): Weight for Sustainable dimension. Default is 0.25.

    Returns:
        float: The calculated Exit-AI-R Score.
    """
    # Ensure weights sum to 1
    total_weight = w_visible + w_documented + w_sustainable
    if not np.isclose(total_weight, 1.0):
        print(f"Warning: Provided weights sum to {total_weight}. Normalizing to 1.")
        w_visible /= total_weight
        w_documented /= total_weight
        w_sustainable /= total_weight

    exit_ai_r_score = (w_visible * visible_score +
                       w_documented * documented_score +
                       w_sustainable * sustainable_score)
    return exit_ai_r_score

# User can optionally override default weights
print("\nEnter weights for Exit-AI-R calculation (press Enter to use defaults):")
try:
    user_w_visible = float(input(f"Weight for Visible (default {0.35:.2f}): ") or 0.35)
    user_w_documented = float(input(f"Weight for Documented (default {0.40:.2f}): ") or 0.40)
    user_w_sustainable = float(input(f"Weight for Sustainable (default {0.25:.2f}): ") or 0.25)
except ValueError:
    print("Invalid weight input. Using default weights.")
    user_w_visible = 0.35
    user_w_documented = 0.40
    user_w_sustainable = 0.25

# Execution: Calculate the Exit-AI-R Score
exit_ai_r_score = calculate_exit_air_score(
    innovatech_scores['Visible'],
    innovatech_scores['Documented'],
    innovatech_scores['Sustainable'],
    w_visible=user_w_visible,
    w_documented=user_w_documented,
    w_sustainable=user_w_sustainable
)

print(f"\n{company_name}'s calculated Exit-AI-R Score is: {exit_ai_r_score:.2f}")
```

### Markdown cell (explanation of execution <only if necessary>)

An Exit-AI-R score of `$${exit_ai_r_score:.2f}$$` for InnovateTech provides a clear, quantitative benchmark for its AI readiness. As a Portfolio Manager, I can use this score to:
1.  **Benchmark**: Compare InnovateTech against other portfolio companies or industry averages.
2.  **Identify Gaps**: A lower score suggests areas where further AI investment or better documentation could enhance value before exit.
3.  **Communicate Value**: This single metric concisely communicates the overall AI maturity to potential buyers and internal stakeholders, setting the stage for valuation discussions.

---

## 4. Projecting Valuation Uplift through AI Premium

### Markdown Cell — Story + Context + Real-World Relevance

With InnovateTech's Exit-AI-R Score in hand, my next crucial task is to translate this qualitative assessment into a tangible financial impact. Buyers are increasingly willing to pay a premium for companies with strong, proven AI capabilities. This section quantifies that potential valuation uplift by applying a multiple attribution model.

The `Multiple Attribution Model` projects the potential exit EBITDA multiple by adding an AI premium to a baseline sector multiple. The premium is directly proportional to the Exit-AI-R Score and a customizable AI premium coefficient ($\delta$), which reflects the market's willingness to reward AI-driven value.

The formula for projecting the valuation multiple is:

$$Multiple_j = Multiple_{base,k} + \delta \cdot \frac{Exit-AI-R_j}{100}$$

Where:
- $Multiple_j$ is the projected valuation multiple for company $j$.
- $Multiple_{base,k}$ is the baseline EBITDA multiple for company $j$'s sector $k$.
- $\delta$ (delta) is the AI premium coefficient (e.g., $1.0$ to $3.0$ turns of EBITDA), representing the maximum potential multiple uplift for a company with a perfect 100 Exit-AI-R Score.
- $Exit-AI-R_j$ is the calculated Exit-AI-R Score for company $j$.

### Code cell (function definition + function execution)

```python
def project_valuation_impact(exit_ai_r_score, baseline_ebitda_multiple, ai_premium_coefficient):
    """
    Projects the potential valuation multiple uplift attributable to the Exit-AI-R score.

    Args:
        exit_ai_r_score (float): The calculated Exit-AI-R Score.
        baseline_ebitda_multiple (float): The baseline EBITDA multiple for the company's sector.
        ai_premium_coefficient (float): The customizable AI premium coefficient (delta, e.g., 1.0 to 3.0 turns).

    Returns:
        float: The projected valuation multiple.
    """
    # Calculate the AI-attributable multiple uplift
    ai_multiple_uplift = (ai_premium_coefficient * exit_ai_r_score) / 100
    
    # Project the new valuation multiple
    projected_multiple = baseline_ebitda_multiple + ai_multiple_uplift
    
    return projected_multiple

def plot_valuation_comparison(baseline_multiple, projected_multiple):
    """
    Generates a bar chart comparing the baseline and projected EBITDA multiples.
    """
    multiples_df = pd.DataFrame({
        'Metric': ['Baseline EBITDA Multiple', 'Projected EBITDA Multiple (with AI Premium)'],
        'Value': [baseline_multiple, projected_multiple]
    })

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Metric', y='Value', data=multiples_df, palette='coolwarm')
    plt.title(f"{company_name}'s Valuation Multiple Comparison")
    plt.ylabel("EBITDA Multiple (x)")
    plt.xlabel("")
    plt.show()

# User input for baseline multiple and AI premium coefficient
print("\nPlease provide inputs for valuation projection:")
while True:
    try:
        baseline_ebitda_multiple = float(input("Baseline EBITDA Multiple for the sector (e.g., 7.0): "))
        if baseline_ebitda_multiple <= 0:
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Please enter a positive number for the baseline multiple.")

while True:
    try:
        ai_premium_coefficient = float(input("AI Premium Coefficient (delta, e.g., 1.0 to 3.0 turns of EBITDA for 100 Exit-AI-R score): "))
        if ai_premium_coefficient < 0:
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Please enter a non-negative number for the AI premium coefficient.")

# Execution: Project the valuation impact
projected_ebitda_multiple = project_valuation_impact(
    exit_ai_r_score,
    baseline_ebitda_multiple,
    ai_premium_coefficient
)

print(f"\nBaseline EBITDA Multiple: {baseline_ebitda_multiple:.2f}x")
print(f"Projected EBITDA Multiple (with AI Premium): {projected_ebitda_multiple:.2f}x")

# Execution: Plot the valuation comparison
plot_valuation_comparison(baseline_ebitda_multiple, projected_ebitda_multiple)
```

### Markdown cell (explanation of execution <only if necessary>)

The comparison between the baseline EBITDA multiple of `$${baseline_ebitda_multiple:.2f}x$$` and the projected multiple of `$${projected_ebitda_multiple:.2f}x$$` clearly demonstrates the tangible financial impact of InnovateTech's AI capabilities. This uplift, driven by the Exit-AI-R score and the chosen AI premium coefficient, represents an additional valuation potential that I, as a Portfolio Manager, can leverage during negotiations. This quantitative evidence is a powerful tool to justify premium pricing and differentiate InnovateTech in a competitive market.

---

## 5. Crafting the Compelling AI Exit Narrative

### Markdown Cell — Story + Context + Real-World Relevance

My final task is to synthesize all the quantitative insights into a compelling, structured AI exit narrative. This narrative isn't just a story; it's a strategic document that helps potential buyers understand the full scope of InnovateTech's AI value, its competitive advantages, and its future potential. By leveraging the calculated scores and projected valuation uplift, I can craft an evidence-based story that maximizes buyer interest and willingness to pay.

The AI exit narrative typically includes these key elements:

1.  **Capability Journey**: Illustrates the evolution of InnovateTech's AI capabilities, highlighting investments and milestones.
2.  **Value Created**: Quantifies the documented financial impact (EBITDA improvements, revenue growth) directly attributable to AI.
3.  **Competitive Position**: Articulates how InnovateTech's AI capabilities provide a competitive moat relative to industry peers.
4.  **Future Potential**: Outlines identified AI opportunities for the next owner, showcasing growth avenues.
5.  **Sustainability**: Emphasizes embedded processes, retained talent, and a robust technology foundation that ensures AI value endures.

### Code cell (function definition + function execution)

```python
def generate_ai_exit_narrative(company_name, exit_ai_r_score,
                                 visible_score, documented_score, sustainable_score,
                                 baseline_multiple, projected_multiple, ai_premium_coefficient):
    """
    Generates a structured outline for an AI exit narrative, populated with key metrics.

    Args:
        company_name (str): Name of the portfolio company.
        exit_ai_r_score (float): The overall Exit-AI-R Score.
        visible_score (float): Score for Visible AI Capabilities.
        documented_score (float): Score for Documented AI Impact.
        sustainable_score (float): Score for Sustainable AI Capabilities.
        baseline_multiple (float): Baseline EBITDA multiple.
        projected_multiple (float): Projected EBITDA multiple with AI premium.
        ai_premium_coefficient (float): The AI premium coefficient (delta).

    Returns:
        str: A multi-line string representing the structured AI exit narrative report.
    """
    narrative = f"""
---
**{company_name}: Quantified AI Exit Narrative Report**
Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}
Prepared by: {persona_name}, {firm_name}
---

**Executive Summary:**
{company_name} demonstrates a strong AI readiness for exit, with an overall **Exit-AI-R Score of {exit_ai_r_score:.2f}**. This robust capability is projected to contribute to a significant valuation uplift, transforming the baseline sector EBITDA multiple of {baseline_multiple:.2f}x to an estimated **{projected_multiple:.2f}x**. This report details the quantitative evidence supporting {company_name}'s compelling AI story.

---

**1. AI Exit-Readiness Assessment Details:**

*   **Overall Exit-AI-R Score**: {exit_ai_r_score:.2f}
    (This score reflects the weighted average of key AI dimensions, indicating overall readiness for buyer scrutiny.)

*   **Dimension Breakdown**:
    *   **Visible AI Capabilities**: {visible_score:.2f}/100
        (Highlights how clearly {company_name}'s AI is integrated into products, services, and tech stack.)
    *   **Documented AI Impact**: {documented_score:.2f}/100
        (Emphasizes quantifiable ROI and EBITDA improvements directly attributed to AI initiatives.)
    *   **Sustainable AI Capabilities**: {sustainable_score:.2f}/100
        (Assesses the embedded nature of AI talent, governance, and scalable processes for long-term value.)

---

**2. Projected Valuation Impact:**

*   **Baseline Sector EBITDA Multiple**: {baseline_multiple:.2f}x
*   **AI Premium Coefficient ($\delta$) Applied**: {ai_premium_coefficient:.2f} turns of EBITDA
*   **Projected EBITDA Multiple**: {projected_multiple:.2f}x
*   **Implied Multiple Uplift**: {(projected_multiple - baseline_multiple):.2f}x
    (This uplift directly translates to increased enterprise value, showcasing AI as a tangible value driver.)

---

**3. Structured AI Exit Narrative Outline:**

This outline provides key talking points and evidence for buyer presentations.

*   **a. Capability Journey: From Concept to Core Strength**
    *   *Insight*: {company_name} has strategically invested in AI, moving from initial pilots to embedding advanced machine learning across core operations, achieving an Exit-AI-R score of {exit_ai_r_score:.2f}. Our journey reflects a deliberate build-out of capabilities, with a strong focus on generating measurable impact.

*   **b. Value Created: Quantifiable Financial Enhancement**
    *   *Insight*: AI initiatives at {company_name} have led to documented financial improvements, reflected in a 'Documented AI Impact' score of {documented_score:.2f}/100. These include X% EBITDA improvements from Y (e.g., predictive analytics, automation), directly contributing to the projected valuation uplift.

*   **c. Competitive Position: AI as a Differentiator**
    *   *Insight*: With a 'Visible AI Capabilities' score of {visible_score:.2f}/100, {company_name}'s AI-powered products and operational efficiencies provide a significant competitive advantage. This defensible moat positions {company_name} as a leader, outpacing peers in innovation and market responsiveness.

*   **d. Future Potential: Growth Levers for the Next Owner**
    *   *Insight*: Beyond current achievements, {company_name} has identified clear avenues for future AI-driven growth. These include expanding AI into new product lines, optimizing supply chains further, or enhancing customer personalization, promising continued value creation for an acquirer.

*   **e. Sustainability: Embedded, Enduring AI Foundation**
    *   *Insight*: {company_name}'s AI capabilities are built on a sustainable foundation, evidenced by a 'Sustainable AI Capabilities' score of {sustainable_score:.2f}/100. This includes a robust data governance framework, a dedicated and skilled AI talent base, and scalable technology infrastructure, ensuring long-term value and seamless integration.

---
"""
    return narrative

# Execution: Generate the AI Exit Narrative
ai_exit_narrative = generate_ai_exit_narrative(
    company_name,
    exit_ai_r_score,
    innovatech_scores['Visible'],
    innovatech_scores['Documented'],
    innovatech_scores['Sustainable'],
    baseline_ebitda_multiple,
    projected_ebitda_multiple,
    ai_premium_coefficient
)

print(ai_exit_narrative)
```

### Markdown cell (explanation of execution <only if necessary>)

This comprehensive narrative report provides Jane with a powerful and structured document for communicating InnovateTech's AI value proposition. It transforms raw scores and financial projections into a persuasive story, addressing buyer concerns about capability, impact, and future growth. This report is invaluable for investor presentations, confidential information memoranda, and internal alignment, ensuring that InnovateTech's AI-driven value is fully recognized and rewarded in the exit process.
