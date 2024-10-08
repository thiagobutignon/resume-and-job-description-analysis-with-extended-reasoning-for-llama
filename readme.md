# Resume and Job Description Analysis with Extended Reasoning

This project leverages Groq-powered LLaMA-3.1 for analyzing resumes and job descriptions with detailed, step-by-step reasoning. The system uses extended self-reflection and verbal reinforcement learning to enhance the accuracy of the output. It is built with Streamlit to enable an interactive web app interface.

---

## Features

- **Extended Reasoning**: Uses dynamic Chain of Thought (CoT) prompting to break down complex queries into individual reasoning steps.
- **Self-Reflection**: The model evaluates its reasoning at regular intervals, backtracking when necessary to improve results.
- **Detailed Output**: The system generates multiple steps and performs self-reflection every 3 steps to ensure high-quality responses.
- **Resume and Job Analysis**: Tailored to analyzing resumes against job descriptions to identify potential matches, gaps, and areas for improvement.

---

## Demo

You can enter a job description and a resume to see a step-by-step analysis of how well they match and get insights on how to improve the alignment.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Git installed

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-job-analysis.git
cd resume-job-analysis
```

### 2. Create and activate a virtual environment (recommended)
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install the required Python packages
```bash
pip install -r requirements.txt
```

### 4. Set up the Groq API Key
You need to set your Groq API key in the environment to enable API access.

1. Open the .env file (if not available, create one in the root of the project).
2. Add your GROQ API Key:
```.env
GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Run the Streamlit App
To start the web app locally, run:

```bash
streamlit run app.py
```

### 6. Access the App
After running the above command, you can access the app in your browser at:
```
http://localhost:8501
```

## How to Use
1. Enter a Job Description: Input the job description you want to analyze.
2. Enter a Resume: Input the resume you want to compare against the job description.
3. View the Results: The app will generate a detailed reasoning chain comparing the resume to the job description, identifying key strengths and areas for improvement.

The app breaks down the analysis into multiple reasoning steps, performing self-reflection at regular intervals to ensure a thorough review.

## Filestructure
```bash
resume-job-analysis/
│
├── app.py               # The main Streamlit app file
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Ignored files
├── .env                  # Environment file for API keys
└── other project files
```
## Troubleshooting
If you encounter any issues:

*API Errors*: Ensure your Groq API key is correctly set in the .env file.
*Environment Issues*: Ensure all required Python packages are installed by running pip install -r requirements.txt.
*Streamlit Issues*: Ensure Streamlit is installed (pip install streamlit), and run streamlit run app.py from the project root directory.

## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments
Special thanks to the Groq team for providing the API and hardware support.