
import pytest
from streamlit.testing.v1 import AppTest
import numpy as np

# Ensure the app code is saved as 'app.py' in the same directory as the test file
# or adjust the path in AppTest.from_file() accordingly.

def get_app_test():
    """Helper to load the app for each test, ensuring a clean state."""
    return AppTest.from_file("app.py")

def test_initial_state_and_default_display():
    """
    Verifies the initial state of the application, including default session state
    variables and the absence of conditional output.
    """
    at = get_app_test().run()

    # Check initial session state values
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

    # Check initial widget values
    assert at.text_input[0].value == "Jane Doe" # Persona Name
    assert at.text_input[1].value == "Alpha Capital" # Firm Name
    assert at.text_input[2].value == "InnovateTech" # Company Name
    assert at.slider[0].value == 75 # Visible AI Capabilities Score
    assert at.slider[1].value == 60 # Documented AI Impact Score
    assert at.slider[2].value == 80 # Sustainable AI Capabilities Score
    assert at.number_input[0].value == 0.35 # Weight for Visible AI
    assert at.number_input[1].value == 0.40 # Weight for Documented AI
    assert at.number_input[2].value == 0.25 # Weight for Sustainable AI
    # Baseline EBITDA Multiple and AI Premium Coefficient are further down, conditionally enabled
    # So we'll check their presence only when appropriate

    # Verify that conditional output is not present initially
    assert not at.markdown.find("InnovateTech's calculated Exit-AI-R Score is").exists
    assert not at.markdown.find("Baseline EBITDA Multiple:").exists
    assert not at.expander("View Generated AI Exit Narrative Report").exists
    assert not at.warning[0].exists # No warnings initially

def test_sidebar_reset_application():
    """
    Tests the 'Reset Application' button in the sidebar.
    """
    at = get_app_test().run()

    # Change some inputs
    at.text_input[0].set_value("John Doe").run()
    at.slider[0].set_value(50).run()
    at.number_input[0].set_value(0.5).run()

    assert at.session_state["persona_name"] == "John Doe"
    assert at.session_state["visible_score"] == 50
    assert at.session_state["w_visible"] == 0.5

    # Click the reset button
    at.button[0].click().run() # The sidebar button is the first button in the app

    # Verify session state is reset to initial defaults
    assert at.session_state["persona_name"] == "Jane Doe"
    assert at.session_state["visible_score"] == 75
    assert at.session_state["w_visible"] == 0.35
    assert at.session_state["exit_ai_r_score"] is None # Should also be cleared

def test_dimension_score_plotting():
    """
    Tests the 'Plot Dimension Scores' button and its effect.
    """
    at = get_app_test().run()

    # Change scores
    at.slider[0].set_value(90).run() # Visible
    at.slider[1].set_value(70).run() # Documented
    at.slider[2].set_value(85).run() # Sustainable

    # Click the plot button (first button in main content)
    at.button[1].click().run() # This button is 'Plot Dimension Scores'

    assert at.session_state.plot_scores_triggered
    # Check if a plot is rendered. AppTest doesn't expose figures directly,
    # but we can check for the presence of st.pyplot output.
    # The plot is generated via st.pyplot, which corresponds to a `pyplot` element in AppTest.
    assert at.pyplot[0].exists
    assert "InnovateTech's AI Exit-Readiness Dimension Scores" in at.pyplot[0].caption # Verify plot title

def test_calculate_exit_air_score():
    """
    Tests the calculation of Exit-AI-R score with default weights.
    """
    at = get_app_test().run()

    # Default scores: Visible=75, Documented=60, Sustainable=80
    # Default weights: w_v=0.35, w_d=0.40, w_s=0.25
    expected_score = (75 * 0.35) + (60 * 0.40) + (80 * 0.25) # 26.25 + 24 + 20 = 70.25

    # Click the calculate button (after plot button)
    at.button[2].click().run() # This button is 'Calculate Exit-AI-R Score'

    assert at.session_state.calculate_air_triggered
    assert np.isclose(at.session_state.exit_ai_r_score, expected_score)
    assert at.markdown.find(f"InnovateTech's calculated Exit-AI-R Score is: **{expected_score:.2f}**").exists

def test_calculate_exit_air_score_with_custom_weights_and_normalization():
    """
    Tests Exit-AI-R score calculation with custom weights, including normalization.
    """
    at = get_app_test().run()

    # Set custom scores and weights
    at.slider[0].set_value(100).run() # Visible
    at.slider[1].set_value(50).run()  # Documented
    at.slider[2].set_value(0).run()   # Sustainable

    at.number_input[0].set_value(0.5).run() # w_visible
    at.number_input[1].set_value(0.3).run() # w_documented
    at.number_input[2].set_value(0.2).run() # w_sustainable
    # Weights sum to 1.0, no normalization needed

    expected_score = (100 * 0.5) + (50 * 0.3) + (0 * 0.2) # 50 + 15 + 0 = 65.0

    at.button[2].click().run() # 'Calculate Exit-AI-R Score'

    assert np.isclose(at.session_state.exit_ai_r_score, expected_score)
    assert at.markdown.find(f"Innovatech's calculated Exit-AI-R Score is: **{expected_score:.2f}**").exists

    # Now test with weights that don't sum to 1.0, expecting normalization
    at.number_input[0].set_value(0.2).run() # w_visible
    at.number_input[1].set_value(0.2).run() # w_documented
    at.number_input[2].set_value(0.1).run() # w_sustainable
    # Weights sum to 0.5. Normalized weights: 0.4, 0.4, 0.2
    expected_score_normalized = (100 * 0.4) + (50 * 0.4) + (0 * 0.2) # 40 + 20 + 0 = 60.0

    at.button[2].click().run() # 'Calculate Exit-AI-R Score' again

    assert at.warning[0].value.startswith("Warning: Provided weights sum to 0.50. Normalizing to 1.0 for calculation.")
    assert np.isclose(at.session_state.exit_ai_r_score, expected_score_normalized)
    assert at.markdown.find(f"Innovatech's calculated Exit-AI-R Score is: **{expected_score_normalized:.2f}**").exists


def test_valuation_projection_without_ai_r_score_warning():
    """
    Tests the warning message when valuation projection is attempted without
    calculating the Exit-AI-R score first.
    """
    at = get_app_test().run()

    # Exit-AI-R score is None by default
    assert at.session_state.exit_ai_r_score is None

    # This section for valuation projection should display a warning
    assert at.warning[0].value == "Please calculate the Exit-AI-R Score in the previous section to proceed with valuation projection."
    # The valuation inputs (number_input and slider) should not be directly accessible or should be greyed out.
    # In AppTest, if widgets are conditional on session_state, they won't be in the list.
    assert not at.number_input.find(key="baseline_ebitda_multiple_input").exists
    assert not at.slider.find(key="ai_premium_coefficient_slider").exists


def test_valuation_projection():
    """
    Tests the projection of valuation uplift with AI premium.
    """
    at = get_app_test().run()

    # First, calculate Exit-AI-R score
    at.button[2].click().run() # 'Calculate Exit-AI-R Score'
    assert at.session_state.exit_ai_r_score is not None

    # Now, valuation inputs should be available
    assert at.number_input.find(key="baseline_ebitda_multiple_input").exists
    assert at.slider.find(key="ai_premium_coefficient_slider").exists

    # Set custom baseline multiple and AI premium coefficient
    at.number_input[3].set_value(8.0).run() # Baseline EBITDA Multiple (number_input[3] assuming previous ones are persona, firm, company, w_visible, w_documented, w_sustainable. Check indices carefully)
    # The indices will be relative to the widgets *visible at that point*.
    # After calculate_air_score, the widgets are:
    # 0,1,2: w_visible, w_documented, w_sustainable
    # 3: baseline_ebitda_multiple_input
    # So, at.number_input[3] is correct.
    at.slider[3].set_value(3.0).run() # AI Premium Coefficient (slider[3] because sliders for visible, documented, sustainable are 0,1,2)

    assert at.session_state.baseline_ebitda_multiple == 8.0
    assert at.session_state.ai_premium_coefficient == 3.0

    # Calculated Exit-AI-R score from previous step (default inputs) was 70.25
    ai_r_score = at.session_state.exit_ai_r_score
    baseline_multiple = 8.0
    premium_coeff = 3.0
    expected_projected_multiple = baseline_multiple + (premium_coeff * ai_r_score / 100) # 8.0 + (3.0 * 70.25 / 100) = 8.0 + 2.1075 = 10.1075

    at.button[3].click().run() # 'Project Valuation Uplift' (after calculate_air and plot_scores)

    assert at.session_state.project_valuation_triggered
    assert np.isclose(at.session_state.projected_ebitda_multiple, expected_projected_multiple)

    assert at.markdown.find(f"- Baseline EBITDA Multiple: **{baseline_multiple:.2f}x**").exists
    assert at.markdown.find(f"- Projected EBITDA Multiple (with AI Premium): **{expected_projected_multiple:.2f}x**").exists

    # Verify valuation comparison plot is rendered
    assert at.pyplot[1].exists
    assert f"InnovateTech's Valuation Multiple Comparison" in at.pyplot[1].caption


def test_narrative_generation_without_valuation_warning():
    """
    Tests the warning message when narrative generation is attempted without
    projecting valuation first.
    """
    at = get_app_test().run()

    # Projected multiple is None by default
    assert at.session_state.projected_ebitda_multiple is None

    # This section for narrative generation should display a warning
    assert at.warning[0].value == "Please complete the valuation projection in the previous section to generate the narrative report."
    # The generate narrative button should not be directly accessible.
    assert not at.button.find(key="generate_narrative_button").exists


def test_narrative_generation():
    """
    Tests the generation of the AI Exit Narrative report.
    """
    at = get_app_test().run()

    # First, calculate Exit-AI-R score
    at.button[2].click().run() # 'Calculate Exit-AI-R Score'

    # Then, project valuation uplift
    at.number_input[3].set_value(8.0).run() # Baseline EBITDA Multiple
    at.slider[3].set_value(3.0).run() # AI Premium Coefficient
    at.button[3].click().run() # 'Project Valuation Uplift'

    assert at.session_state.projected_ebitda_multiple is not None

    # Click 'Generate AI Exit Narrative' button
    at.button[4].click().run() # This is the last button

    assert at.session_state.generate_narrative_triggered
    assert at.expander("View Generated AI Exit Narrative Report").exists
    assert at.expander("View Generated AI Exit Narrative Report").expanded

    narrative_markdown = at.expander("View Generated AI Exit Narrative Report").markdown[0].value

    # Verify key elements in the generated narrative
    assert "InnovateTech: Quantified AI Exit Narrative Report" in narrative_markdown
    assert f"Prepared by: {at.session_state.persona_name}, {at.session_state.firm_name}" in narrative_markdown
    assert f"Overall Exit-AI-R Score: {at.session_state.exit_ai_r_score:.2f}" in narrative_markdown
    assert f"Baseline Sector EBITDA Multiple: {at.session_state.baseline_ebitda_multiple:.2f}x" in narrative_markdown
    assert f"Projected EBITDA Multiple (with AI Premium): {at.session_state.projected_ebitda_multiple:.2f}x" in narrative_markdown
    assert f"Implied Multiple Uplift: {(at.session_state.projected_ebitda_multiple - at.session_state.baseline_ebitda_multiple):.2f}x" in narrative_markdown
    assert f"Visible AI Capabilities Score: {at.session_state.visible_score:.0f}/100" in narrative_markdown

