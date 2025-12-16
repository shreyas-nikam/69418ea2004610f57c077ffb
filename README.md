# QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

The "QuLab: Exit-Readiness AI Narrative & Valuation Impact Calculator" is a Streamlit application designed for portfolio managers and private equity professionals to systematically assess a portfolio company's AI capabilities from an M&A exit perspective. It quantifies the potential valuation uplift attributable to AI maturity and generates a compelling, data-driven narrative for potential strategic and financial buyers.

In today's competitive market, a strong, well-articulated AI narrative can significantly enhance a company's perceived value, attracting premium valuations during an exit event. This application guides users through a structured workflow to evaluate AI across critical dimensions, calculate an overall "Exit-AI-R Score," project its financial impact on EBITDA multiples, and synthesize these insights into a persuasive report.

## Features

This application offers a guided, interactive workflow with the following key features:

*   **Persona & Company Customization**: Define the user's role (e.g., Portfolio Manager), firm, and the target portfolio company for a personalized experience.
*   **Structured AI Capability Assessment**: Evaluate the target company's AI capabilities across three crucial dimensions:
    *   **Visible AI Capabilities**: How perceivable AI is in products/services.
    *   **Documented AI Impact**: Proven financial ROI and impact from AI investments.
    *   **Sustainable AI Capabilities**: Deep integration, governance, and talent for long-term AI value.
*   **Interactive Score Plotting**: Visualize the scores for each AI dimension using bar charts.
*   **Weighted Exit-AI-R Score Calculation**: Compute an overall AI Readiness Score using user-defined weights for each dimension, reflecting different buyer priorities or market dynamics. The application handles weight normalization.
*   **Valuation Impact Projection**: Project the potential uplift in the company's EBITDA multiple by incorporating the calculated Exit-AI-R Score and a configurable AI Premium Coefficient ($\\delta$).
*   **Valuation Comparison Plotting**: Visualize the difference between the baseline and projected EBITDA multiples.
*   **Comprehensive AI Exit Narrative Generation**: Automatically generate a detailed report summarizing all assessments, scores, and financial projections into a persuasive, investor-ready narrative.
*   **Session State Persistence**: Maintain user inputs and results across interactions without requiring recalculations until parameters are changed.
*   **Application Reset Functionality**: A convenient sidebar button to clear all inputs and reset the application to its default state.

## Getting Started

Follow these instructions to set up and run the Streamlit application on your local machine.

### Prerequisites

You need Python 3.8+ installed on your system.
The application relies on the following Python libraries:

*   `streamlit`
*   `pandas`
*   `numpy`
*   `matplotlib`
*   `seaborn`

### Installation

1.  **Clone the repository (or save the code):**
    If this code is part of a Git repository, clone it:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    Otherwise, save the provided Python code as `app.py` in a directory of your choice.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install streamlit pandas numpy matplotlib seaborn
    ```

## Usage

To run the application, navigate to the directory containing `app.py` in your terminal and execute:

```bash
streamlit run app.py
```

This command will open the Streamlit application in your default web browser (usually `http://localhost:8501`).

### Basic Workflow:

1.  **1. Setting the Stage: InnovateTech's Exit Readiness**:
    *   Enter/confirm the `Persona Name`, `Firm Name`, and `Company Name` for the scenario.
2.  **2. Assessing InnovateTech's AI Exit-Readiness Dimensions**:
    *   Use the sliders to rate the company on **Visible**, **Documented**, and **Sustainable** AI capabilities (0-100).
    *   Click "Plot Dimension Scores" to visualize the individual scores.
3.  **3. Calculating the Overall Exit-AI-R Score**:
    *   Adjust the weights ($w_1, w_2, w_3$) for each AI dimension to reflect their relative importance. The application will normalize weights if they don't sum to 1.0.
    *   Click "Calculate Exit-AI-R Score" to get the overall weighted score.
4.  **4. Projecting Valuation Uplift through AI Premium**:
    *   Enter a `Baseline EBITDA Multiple` for the sector.
    *   Adjust the `AI Premium Coefficient (δ)` to model market enthusiasm for AI.
    *   Click "Project Valuation Uplift" to see the new projected EBITDA multiple and its visual comparison.
5.  **5. Crafting the Compelling AI Exit Narrative**:
    *   Click "Generate AI Exit Narrative" to produce a comprehensive report based on all your inputs and calculations. The report will appear in an expandable section.
6.  **Reset Application**: Use the "Reset Application" button in the sidebar to clear all inputs and start fresh.

## Project Structure

The project currently consists of a single Python file, `app.py`, which encapsulates all the application logic, UI elements, and data visualization.

```
.
├── app.py                  # Main Streamlit application file
└── README.md               # This README file
```

Within `app.py`, the code is organized into logical sections:

*   **Imports & Configuration**: Library imports, warning suppression, and Streamlit page settings.
*   **Sidebar & Session State Initialization**: Defines sidebar elements like the reset button and initializes all session state variables for persistence.
*   **Main Application Title & Introduction**: Sets the app's title and provides a business context.
*   **Utility Functions**: `@st.cache_data` decorated functions for plotting and calculations to optimize performance.
*   **Streamlit UI Layout (Sections 1-5)**: Organizes the interactive components and displays results in a logical flow:
    *   Section 1: Persona & Company Setup
    *   Section 2: AI Dimension Assessment
    *   Section 3: Exit-AI-R Score Calculation
    *   Section 4: Valuation Projection
    *   Section 5: Narrative Generation
*   **Footer**: Final contact/acknowledgment.

## Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: For building interactive web applications with pure Python.
*   **Pandas**: For data manipulation, especially useful for preparing data for plots.
*   **NumPy**: For numerical operations, particularly in score calculations.
*   **Matplotlib**: For generating static, embeddable visualizations.
*   **Seaborn**: Built on Matplotlib, providing a high-level interface for drawing attractive statistical graphics.

## Contributing

This project is primarily designed as a lab/educational exercise. However, contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes and ensure they adhere to the existing code style.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (or assume MIT if not explicitly created).

```
MIT License

Copyright (c) [Year] [Your Name or QuantUniversity]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact

For questions or inquiries, please contact:

*   **Organization**: QuantUniversity
*   **Website**: [https://www.quantuniversity.com](https://www.quantuniversity.com)
*   **Email**: info@quantuniversity.com
