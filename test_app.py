
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import numpy as np

# A helper function to load the app for each test
def get_app_test_instance():
    """Loads the Streamlit app from app.py."""
    return AppTest.from_file("app.py")

def test_1_initial_load_and_default_state():
    """
    Tests the initial loading of the app, default session state values,
    and initial display on Page 1.
    """
    at = get_app_test_instance().run()

    # Check initial values in session state
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
    assert at.session_state["plot_scores_triggered"] is False
    assert at.session_state["calculate_air_triggered"] is False
    assert at.session_state["project_valuation_triggered"] is False
    assert at.session_state["generate_narrative_triggered"] is False

    # Check initial page content (Page 1: "1. Setting the Stage")
    assert at.header[0].value == "1. Setting the Stage: InnovateTech's Exit Readiness"
    assert "Jane Doe, a Portfolio Manager at Alpha Capital" in at.markdown[1].value
    assert "InnovateTech" in at.markdown[1].value

    # Check text inputs reflect default session state
    assert at.text_input[0].value == "Jane Doe"
    assert at.text_input[1].value == "Alpha Capital"
    assert at.text_input[2].value == "InnovateTech"

def test_2_page1_persona_and_company_details_update():
    """
    Tests updating persona and company details on Page 1 and verifying session state.
    """
    at = get_app_test_instance().run()

    # Update persona and company details via text inputs
    at.text_input[0].set_value("John Smith").run()
    at.text_input[1].set_value("Beta Ventures").run()
    at.text_input[2].set_value("QuantumFlow").run()

    # Verify session state is updated
    assert at.session_state["persona_name"] == "John Smith"
    assert at.session_state["firm_name"] == "Beta Ventures"
    assert at.session_state["company_name"] == "QuantumFlow"

    # Verify updated values are reflected in the markdown on the page
    assert "John Smith, a Portfolio Manager at Beta Ventures" in at.markdown[1].value
    assert "QuantumFlow" in at.markdown[1].value
    assert "Now that the context is set, I'm ready to dive into assessing QuantumFlow's AI capabilities." in at.markdown[3].value

def test_3_page2_assessment_and_plot():
    """
    Tests interaction with sliders and the plotting functionality on Page 2.
    """
    at = get_app_test_instance().run()
    
    # Navigate to "2. Assessing AI Dimensions"
    at.selectbox[0].set_value("2. Assessing AI Dimensions").run()

    assert at.header[0].value == "2. Assessing InnovateTech's AI Exit-Readiness Dimensions"
    assert "InnovateTech's AI value proposition" in at.markdown[1].value

    # Check default slider values
    assert at.slider[0].value == 75 # Visible AI Capabilities Score
    assert at.slider[1].value == 60 # Documented AI Impact Score
    assert at.slider[2].value == 80 # Sustainable AI Capabilities Score

    # Change slider values
    at.slider[0].set_value(90).run() # Visible
    at.slider[1].set_value(70).run() # Documented
    at.slider[2].set_value(95).run() # Sustainable

    # Verify session state updates
    assert at.session_state["visible_score"] == 90
    assert at.session_state["documented_score"] == 70
    assert at.session_state["sustainable_score"] == 95

    # Click the "Plot Dimension Scores" button
    at.button[0].click().run()

    # Verify plot is rendered by checking the pyplot component count and its caption
    assert len(at.pyplot) == 1
    assert at.pyplot[0] is not None
    assert "InnovateTech's AI Exit-Readiness Dimension Scores" in at.pyplot[0].props["caption"]
    assert at.session_state["plot_scores_triggered"] is True

def test_4_page3_calculate_air_score():
    """
    Tests weight inputs, calculation of Exit-AI-R score, and warning for non-normalized weights on Page 3.
    """
    at = get_app_test_instance().run()
    
    # Navigate to "3. Calculating Exit-AI-R Score"
    at.selectbox[0].set_value("3. Calculating Exit-AI-R Score").run()

    assert at.header[0].value == "3. Calculating the Overall Exit-AI-R Score"
    assert "Exit-AI-R Score is a crucial metric" in at.markdown[1].value

    # Check default weights
    assert at.number_input[0].value == 0.35 # w_visible
    assert at.number_input[1].value == 0.40 # w_documented
    assert at.number_input[2].value == 0.25 # w_sustainable

    # Change weights (sum to 1.0)
    at.number_input[0].set_value(0.4).run()
    at.number_input[1].set_value(0.3).run()
    at.number_input[2].set_value(0.3).run()

    # Click "Calculate Exit-AI-R Score" button
    at.button[0].click().run()

    # Verify score in session state (using default scores from app.py: 75, 60, 80)
    # Expected score: 0.4 * 75 + 0.3 * 60 + 0.3 * 80 = 30 + 18 + 24 = 72
    assert at.session_state["exit_ai_r_score"] == pytest.approx(72.0)
    
    # Verify displayed score in markdown
    assert f"InnovateTech's calculated Exit-AI-R Score is: **{72.0:.2f}**" in at.markdown[3].value
    assert at.session_state["calculate_air_triggered"] is True
    assert len(at.warning) == 0 # No warning should be present for sum=1.0

    # Test with non-normalized weights
    at.number_input[0].set_value(0.5).run()
    at.number_input[1].set_value(0.5).run()
    at.number_input[2].set_value(0.5).run() # Sums to 1.5

    at.button[0].click().run() # Recalculate

    # Verify warning is shown for non-normalized weights
    assert len(at.warning) == 1
    assert "Warning: Provided weights sum to 1.50. Normalizing to 1.0 for calculation." in at.warning[0].value

    # Check calculated score after normalization (using default scores 75, 60, 80)
    # Normalized weights: 0.5/1.5, 0.5/1.5, 0.5/1.5 = 1/3, 1/3, 1/3
    # (1/3) * 75 + (1/3) * 60 + (1/3) * 80 = 25 + 20 + 26.666... = 71.666...
    assert at.session_state["exit_ai_r_score"] == pytest.approx((75+60+80)/3)

def test_5_page4_valuation_projection():
    """
    Tests inputs, projection calculation, and plotting of valuation on Page 4.
    """
    at = get_app_test_instance().run()
    
    # Set necessary session state values directly for isolated testing of this page
    at.session_state["exit_ai_r_score"] = 72.0 # Simulate prior calculation
    at.session_state["baseline_ebitda_multiple"] = 7.0
    at.session_state["ai_premium_coefficient"] = 2.0
    at.session_state["project_valuation_triggered"] = False

    # Navigate to "4. Projecting Valuation Uplift"
    at.selectbox[0].set_value("4. Projecting Valuation Uplift").run()

    assert at.header[0].value == "4. Projecting Valuation Uplift through AI Premium"
    assert "translating InnovateTech's AI readiness into a financial impact" in at.markdown[1].value

    # Check default inputs
    assert at.number_input[0].value == 7.0 # Baseline EBITDA Multiple
    assert at.slider[0].value == 2.0 # AI Premium Coefficient

    # Change inputs
    at.number_input[0].set_value(8.5).run()
    at.slider[0].set_value(3.0).run()

    # Click "Project Valuation Uplift" button
    at.button[0].click().run()

    # Calculate expected projected multiple: baseline + (coeff * score / 100)
    # 8.5 + (3.0 * 72.0 / 100) = 8.5 + (216 / 100) = 8.5 + 2.16 = 10.66
    expected_projected_multiple = 8.5 + (3.0 * 72.0 / 100)
    assert at.session_state["projected_ebitda_multiple"] == pytest.approx(expected_projected_multiple)

    # Verify displayed multiples in markdown
    assert f"**Baseline EBITDA Multiple**: **{8.5:.2f}x**" in at.markdown[3].value
    assert f"**Projected EBITDA Multiple (with AI Premium)**: **{expected_projected_multiple:.2f}x**" in at.markdown[4].value
    assert at.session_state["project_valuation_triggered"] is True

    # Verify plot is rendered (assuming it's the first pyplot if no other pages rendered one)
    # Note: AppTest accumulates pyplot calls across runs.
    # If a previous test rendered a plot (e.g., test_3_page2_assessment_and_plot),
    # then len(at.pyplot) might be > 1. We look for the last one.
    assert len(at.pyplot) >= 1 # At least one plot, specific to this page
    assert at.pyplot[-1] is not None
    assert "InnovateTech's Valuation Multiple Comparison" in at.pyplot[-1].props["caption"]

def test_6_page4_valuation_projection_without_air_score_warning():
    """
    Tests the warning displayed on Page 4 if Exit-AI-R Score has not been calculated.
    """
    at = get_app_test_instance().run()
    
    # Ensure exit_ai_r_score is None
    at.session_state["exit_ai_r_score"] = None 

    # Navigate to "4. Projecting Valuation Uplift"
    at.selectbox[0].set_value("4. Projecting Valuation Uplift").run()

    # Verify warning is displayed
    assert len(at.warning) == 1
    assert "Please calculate the Exit-AI-R Score in the '3. Calculating Exit-AI-R Score' section to proceed with valuation projection." in at.warning[0].value
    
    # Ensure valuation-related widgets are NOT displayed
    assert len(at.number_input) == 0
    assert len(at.slider) == 0
    assert len(at.button) == 0

def test_7_page5_narrative_generation():
    """
    Tests narrative generation on Page 5, including checking for key content.
    """
    at = get_app_test_instance().run()
    
    # Set necessary session state values directly for isolated testing of this page
    at.session_state["persona_name"] = "John Smith"
    at.session_state["firm_name"] = "Beta Ventures"
    at.session_state["company_name"] = "QuantumFlow"
    at.session_state["exit_ai_r_score"] = 72.0
    at.session_state["visible_score"] = 75
    at.session_state["documented_score"] = 60
    at.session_state["sustainable_score"] = 80
    at.session_state["baseline_ebitda_multiple"] = 8.5
    at.session_state["ai_premium_coefficient"] = 3.0
    at.session_state["projected_ebitda_multiple"] = 10.66
    at.session_state["generate_narrative_triggered"] = False

    # Navigate to "5. Crafting the Exit Narrative"
    at.selectbox[0].set_value("5. Crafting the Exit Narrative").run()

    assert at.header[0].value == "5. Crafting the Compelling AI Exit Narrative"
    assert "synthesize these quantitative insights into a structured, persuasive narrative" in at.markdown[1].value

    # Click "Generate AI Exit Narrative" button
    at.button[0].click().run()

    # Verify narrative text is present in an expander and check its content
    assert at.expander[0].label == "View Generated AI Exit Narrative Report"
    narrative_content = at.expander[0].markdown[0].value

    assert "QuantumFlow: Quantified AI Exit Narrative Report" in narrative_content
    assert "Prepared by: John Smith, Beta Ventures" in narrative_content
    assert f"Exit-AI-R Score of {at.session_state['exit_ai_r_score']:.2f}" in narrative_content
    assert f"baseline sector EBITDA multiple of {at.session_state['baseline_ebitda_multiple']:.2f}x to an estimated **{at.session_state['projected_ebitda_multiple']:.2f}x**." in narrative_content
    assert f"Visible AI Capabilities: {at.session_state['visible_score']:.2f}/100" in narrative_content
    assert f"AI Premium Coefficient ($\delta$): {at.session_state['ai_premium_coefficient']:.2f} turns" in narrative_content
    
    # Implied Multiple Uplift: projected - baseline
    implied_uplift = at.session_state['projected_ebitda_multiple'] - at.session_state['baseline_ebitda_multiple']
    assert f"Implied Multiple Uplift: {implied_uplift:.2f}x" in narrative_content
    
    assert f"Developed for Beta Ventures by John Smith." in at.caption[0].value
    assert at.session_state["generate_narrative_triggered"] is True

def test_8_page5_narrative_generation_without_valuation_warning():
    """
    Tests the warning displayed on Page 5 if valuation projection has not been completed.
    """
    at = get_app_test_instance().run()
    
    # Ensure projected_ebitda_multiple is None
    at.session_state["projected_ebitda_multiple"] = None 

    # Navigate to "5. Crafting the Exit Narrative"
    at.selectbox[0].set_value("5. Crafting the Exit Narrative").run()

    # Verify warning is displayed
    assert len(at.warning) == 1
    assert "Please complete the valuation projection in the '4. Projecting Valuation Uplift' section to generate the narrative report." in at.warning[0].value
    
    # Ensure the narrative generation button is NOT displayed
    assert len(at.button) == 0

def test_9_reset_application():
    """
    Tests the "Reset Application" button functionality.
    """
    at = get_app_test_instance().run()

    # Change some session state values to non-default
    at.text_input[0].set_value("Temp User").run()
    at.session_state["visible_score"] = 10
    at.session_state["exit_ai_r_score"] = 50.0
    at.session_state["plot_scores_triggered"] = True

    # Ensure changes are reflected
    assert at.session_state["persona_name"] == "Temp User"
    assert at.session_state["visible_score"] == 10
    assert at.session_state["exit_ai_r_score"] == 50.0
    assert at.session_state["plot_scores_triggered"] is True

    # Click "Reset Application" button in sidebar (it's the first button in sidebar)
    at.sidebar.button[0].click().run()

    # Verify session state is cleared and re-initialized to defaults
    # (AppTest's .run() after .clear() simulates a full rerun)
    assert at.session_state["persona_name"] == "Jane Doe"
    assert at.session_state["firm_name"] == "Alpha Capital"
    assert at.session_state["company_name"] == "InnovateTech"
    assert at.session_state["visible_score"] == 75
    assert at.session_state["exit_ai_r_score"] is None
    assert at.session_state["plot_scores_triggered"] is False # Should be reset

    # Also verify content of the initial page to confirm full reset
    assert at.header[0].value == "1. Setting the Stage: InnovateTech's Exit Readiness"

def test_10_full_application_workflow():
    """
    Tests a complete end-to-end user workflow through all pages of the application.
    """
    at = get_app_test_instance().run()

    # --- Page 1: Setup and Introduction ---
    at.text_input[0].set_value("Alice User").run()
    at.text_input[1].set_value("AI Ventures").run()
    at.text_input[2].set_value("SynergyAI").run()
    assert at.session_state["persona_name"] == "Alice User"
    assert at.session_state["company_name"] == "SynergyAI"

    # --- Page 2: Assessing AI Dimensions ---
    at.selectbox[0].set_value("2. Assessing AI Dimensions").run()
    at.slider[0].set_value(85).run() # Visible
    at.slider[1].set_value(70).run() # Documented
    at.slider[2].set_value(90).run() # Sustainable
    assert at.session_state["visible_score"] == 85
    assert at.session_state["documented_score"] == 70
    assert at.session_state["sustainable_score"] == 90
    at.button[0].click().run() # Plot scores
    assert len(at.pyplot) == 1
    assert at.pyplot[0] is not None
    assert "SynergyAI's AI Exit-Readiness Dimension Scores" in at.pyplot[0].props["caption"]
    assert at.session_state["plot_scores_triggered"] is True

    # --- Page 3: Calculating Exit-AI-R Score ---
    at.selectbox[0].set_value("3. Calculating Exit-AI-R Score").run()
    at.number_input[0].set_value(0.4).run() # w_visible
    at.number_input[1].set_value(0.3).run() # w_documented
    at.number_input[2].set_value(0.3).run() # w_sustainable
    at.button[0].click().run() # Calculate score
    
    # Expected score: (0.4 * 85) + (0.3 * 70) + (0.3 * 90) = 34 + 21 + 27 = 82
    expected_air_score = (0.4 * 85) + (0.3 * 70) + (0.3 * 90)
    assert at.session_state["exit_ai_r_score"] == pytest.approx(expected_air_score)
    assert f"SynergyAI's calculated Exit-AI-R Score is: **{expected_air_score:.2f}**" in at.markdown[3].value
    assert len(at.warning) == 0
    assert at.session_state["calculate_air_triggered"] is True

    # --- Page 4: Projecting Valuation Uplift ---
    at.selectbox[0].set_value("4. Projecting Valuation Uplift").run()
    at.number_input[0].set_value(9.0).run() # Baseline EBITDA
    at.slider[0].set_value(2.5).run() # AI Premium Coefficient
    at.button[0].click().run() # Project valuation

    # Expected projected multiple: 9.0 + (2.5 * 82 / 100) = 9.0 + (205 / 100) = 9.0 + 2.05 = 11.05
    expected_proj_multiple = at.session_state["baseline_ebitda_multiple"] + \
                             (at.session_state["ai_premium_coefficient"] * 
                              at.session_state["exit_ai_r_score"] / 100)
    assert at.session_state["projected_ebitda_multiple"] == pytest.approx(expected_proj_multiple)
    assert f"**Projected EBITDA Multiple (with AI Premium)**: **{expected_proj_multiple:.2f}x**" in at.markdown[4].value
    assert at.session_state["project_valuation_triggered"] is True
    
    # AppTest collects all pyplot calls. The last one should be the valuation plot.
    assert len(at.pyplot) == 2 # One from page 2, one from page 4
    assert at.pyplot[-1] is not None
    assert "SynergyAI's Valuation Multiple Comparison" in at.pyplot[-1].props["caption"]

    # --- Page 5: Crafting the Exit Narrative ---
    at.selectbox[0].set_value("5. Crafting the Exit Narrative").run()
    at.button[0].click().run() # Generate narrative

    assert at.expander[0].label == "View Generated AI Exit Narrative Report"
    narrative_content = at.expander[0].markdown[0].value
    assert "SynergyAI: Quantified AI Exit Narrative Report" in narrative_content
    assert f"Prepared by: Alice User, AI Ventures" in narrative_content
    assert f"Exit-AI-R Score of {expected_air_score:.2f}" in narrative_content
    assert f"baseline sector EBITDA multiple of {at.session_state['baseline_ebitda_multiple']:.2f}x to an estimated **{expected_proj_multiple:.2f}x**." in narrative_content
    
    implied_uplift = expected_proj_multiple - at.session_state['baseline_ebitda_multiple']
    assert f"Implied Multiple Uplift: {implied_uplift:.2f}x" in narrative_content
    assert f"Developed for AI Ventures by Alice User." in at.caption[0].value
    assert at.session_state["generate_narrative_triggered"] is True
