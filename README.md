# QuLab: AI Exit-Readiness & Valuation Impact Calculator

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Title and Description

**QuLab: AI Exit-Readiness & Valuation Impact Calculator** is a sophisticated Streamlit application designed for portfolio managers to systematically assess, quantify, and articulate the AI capabilities of their portfolio companies. In today's M&A landscape, a strong AI narrative is a significant value driver. This application guides users through an end-to-end scenario, demonstrating how to apply AI concepts and analytical tools to make informed decisions that directly impact a company's exit strategy and valuation.

The application emulates the workflow of a portfolio manager, such as Jane Doe from Alpha Capital, preparing a company like InnovateTech for a successful exit. It helps in:

*   **Systematically Assessing InnovateTech's AI Capabilities**: Evaluating the company's AI across key dimensions: Visible, Documented, and Sustainable.
*   **Quantifying AI Readiness**: Calculating a comprehensive Exit-AI-R Score by weighting these dimensions according to market priorities.
*   **Projecting Valuation Uplift**: Modeling the potential impact of this AI readiness on InnovateTech's EBITDA multiple.
*   **Crafting a Data-Driven Narrative**: Generating a persuasive report for strategic and financial buyers, leveraging quantitative analysis.

## Features

*   **Interactive AI Assessment**: Intuitive forms and sliders for evaluating AI capabilities across multiple dimensions (Visible, Documented, Sustainable AI).
*   **Dynamic Score Calculation**: Real-time calculation of the "Exit-AI-R Score" based on user inputs and market weighting.
*   **Valuation Impact Modeling**: Tools to project how AI readiness translates into a tangible uplift in EBITDA multiples and overall company valuation.
*   **Narrative Generation**: Features to help users craft a compelling, data-backed AI exit narrative suitable for potential buyers.
*   **Guided Workflow**: A clear, multi-page navigation structure that leads the user through the entire assessment and strategy development process.
*   **Session State Management**: Ensures user inputs and calculated results persist across different pages of the application.
*   **Application Reset**: A convenient button in the sidebar to clear all session data and restart the assessment.

## Getting Started

Follow these instructions to set up and run the QuLab application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/qu_lab_app.git
    cd qu_lab_app
    ```
    *(Note: Replace `https://github.com/your-username/qu_lab_app.git` with the actual repository URL)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file in the root directory of the project with the following content:
    ```
    streamlit
    # Add any other libraries used in sub-pages, e.g.,
    # pandas
    # numpy
    ```
    Then, install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, navigate to the project's root directory in your terminal and execute the following command:

```bash
streamlit run app.py
```

This command will open the Streamlit application in your default web browser.

### Basic Usage Instructions:

1.  **Navigation**: Use the "Navigation" selectbox in the left sidebar to move between the different stages of the AI exit-readiness assessment.
2.  **Input Data**: Follow the prompts on each page to input relevant information regarding the portfolio company's AI capabilities.
3.  **Interact**: Use sliders, text inputs, and buttons to interact with the application and see dynamic updates to scores and projections.
4.  **Reset**: If you wish to clear all current progress and start over, click the "Reset Application" button in the sidebar.

## Project Structure

The project is organized to provide a clear separation of concerns, with the main application logic in `app.py` and individual workflow steps encapsulated in their own page modules.

```
qu_lab_app/
├── app.py                      # Main Streamlit application entry point
├── utils.py                    # Utility functions, e.g., session state initialization
├── requirements.txt            # Python dependencies
└── application_pages/
    ├── __init__.py             # Makes application_pages a Python package
    ├── page_1_setup.py         # Handles initial setup and introduction
    ├── page_2_assess_dimensions.py # Focuses on assessing AI dimensions
    ├── page_3_calculate_score.py   # Calculates the Exit-AI-R Score
    ├── page_4_project_valuation.py # Models valuation uplift
    └── page_5_craft_narrative.py   # Assists in crafting the AI exit narrative
```

*   **`app.py`**: Orchestrates the multi-page application, handles global session state, and manages overall navigation. It imports pages from `application_pages`.
*   **`utils.py`**: Contains shared functions or variables used across different parts of the application, such as functions to initialize or manage `st.session_state`.
*   **`application_pages/`**: A directory containing separate Python files for each distinct page or step in the application's workflow, making the project modular and easier to manage.

## Technology Stack

*   **Python 3.x**: The core programming language.
*   **Streamlit**: The framework used for building the interactive web application.
*   **(Potentially other libraries)**: Depending on the specific calculations and data manipulations within the individual page modules, libraries like `pandas`, `numpy`, `scipy`, etc., might be used.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: Create a `LICENSE` file in the root directory if you haven't already.)*

## Contact

For questions, feedback, or collaborations, please reach out to:

*   **QuantUniversity**
*   **Website**: [www.quantuniversity.com](https://www.quantuniversity.com/)
*   **Email**: info@quantuniversity.com (Example, update as needed)