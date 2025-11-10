# Healthcare Diagnostic Crew

This project implements a multi-agent AI system using **CrewAI** to simulate a healthcare diagnostic and care coordination workflow. The system takes patient information, symptoms, and medical history as input, and leverages a crew of specialized AI agents to produce a comprehensive diagnostic and care plan.

## How it Works

The project is built around a sequential **CrewAI** workflow. When `main.py` is executed, it kicks off a process involving four distinct AI agents, each with a specific role. The tasks and agents are defined in `tasks.yaml` and `agents.yaml` respectively.

### The Crew

1.  **Symptom Analyzer**:
    * **Role**: Senior Medical Symptom Analyst.
    * **Goal**: To thoroughly analyze the patient's symptoms, evaluate their severity, and identify potential underlying conditions.
    * **Tool**: Uses a `SymptomCheckerTool` to perform a basic assessment.

2.  **Diagnostic Specialist**:
    * **Role**: Board-Certified Diagnostic Specialist.
    * **Goal**: To refine the potential diagnoses from the first agent and recommend appropriate diagnostic tests.
    * **Tool**: Uses a `MedicalGuidelineTool` to look up guidelines for conditions.

3.  **Treatment Advisor**:
    * **Role**: Healthcare Treatment Advisor.
    * **Goal**: To provide evidence-based treatment recommendations and preventive measures based on the refined diagnosis.
    * **Tool**: Also uses the `MedicalGuidelineTool` to ensure recommendations are aligned with current standards.

4.  **Care Coordinator**:
    * **Role**: Patient Care Coordinator.
    * **Goal**: To create a comprehensive care plan, including follow-up schedules, patient instructions, and warning signs for emergency care.
    * **Tool**: This agent does not use custom tools; it synthesizes the information from all previous steps.

## Technologies Used

* **crewai**: For creating and managing the multi-agent system.
* **crewai-tools**: For the base tool classes.
* **google-generativeai**: To power the agents with Google's Gemini models (specifically `gemini-2.0-flash` as configured in `crew.py`).
* **PyYAML**: For loading the agent and task configurations from `.yaml` files.
* **python-dotenv**: To manage environment variables, particularly the API key.
* **Pydantic**: Used to define the input schemas for the custom tools.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/govind2880/healthcare_diagnostic_crew.git](https://github.com/govind2880/healthcare_diagnostic_crew.git)
    cd healthcare_diagnostic_crew
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
   

4.  **Set up your environment variables:**
    * Create a file named `.env` in the root directory.
    * Add your Google Gemini API key to this file, as required by `crew.py`:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

## Usage

To run the diagnostic crew, simply execute the `main.py` script.

```bash
python main.py

The script will use the sample patient data defined in main.py to start the workflow:

Patient Info: '45-year-old male, non-smoker, occasional alcohol'

Symptoms: 'Persistent headache for 3 days, blurred vision, nausea'

Medical History: 'Mild hypertension, family history of migraines'
```

The crew will then run sequentially, with each agent's output being passed as context to the next, ultimately printing a final, comprehensive report to the console.

**Configuration**
This project is highly configurable without changing the Python code:

**Agents:** You can modify the roles, goals, and backstories of the agents by editing agents.yaml.

**Tasks:** The descriptions, expected outputs, and dependencies of each task can be adjusted in tasks.yaml.

**Tools:** Custom tools are defined in tools/custom_tools.py. The current tools are mock implementations, but they can be expanded to connect to real medical APIs or databases.

**License**
This project is licensed under the MIT License. See the LICENSE file for details.