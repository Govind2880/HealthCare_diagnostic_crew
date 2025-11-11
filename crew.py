from crewai import Agent, Task, Crew, Process
from crewai import LLM
from yaml import safe_load
from tools.custom_tools import SymptomCheckerTool, MedicalGuidelineTool
import os
from dotenv import load_dotenv

load_dotenv()

class HealthcareDiagnosticCrew:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = LLM(
            model="gemini/gemini-2.0-flash",
            api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Load agents and tasks from YAML
        self.agents_config = self._load_yaml('agents.yaml')
        self.tasks_config = self._load_yaml('tasks.yaml')
        
        # Initialize tools
        self.symptom_checker = SymptomCheckerTool()
        self.guideline_lookup = MedicalGuidelineTool()
    
    def _load_yaml(self, file_path):
        with open(file_path, 'r') as file:
            return safe_load(file)
    
    def create_agents(self):
        """Create agents from YAML configuration"""
        agents = {}
        
        # Symptom Analyzer Agent
        agents['symptom_analyzer'] = Agent(
            role=self.agents_config['symptom_analyzer']['role'],
            goal=self.agents_config['symptom_analyzer']['goal'],
            backstory=self.agents_config['symptom_analyzer']['backstory'],
            tools=[self.symptom_checker],
            llm=self.llm,
            verbose=True
        )
        
        # Diagnostic Specialist Agent
        agents['diagnostic_specialist'] = Agent(
            role=self.agents_config['diagnostic_specialist']['role'],
            goal=self.agents_config['diagnostic_specialist']['goal'],
            backstory=self.agents_config['diagnostic_specialist']['backstory'],
            tools=[self.guideline_lookup],
            llm=self.llm,
            verbose=True
        )
        
        # Treatment Advisor Agent
        agents['treatment_advisor'] = Agent(
            role=self.agents_config['treatment_advisor']['role'],
            goal=self.agents_config['treatment_advisor']['goal'],
            backstory=self.agents_config['treatment_advisor']['backstory'],
            tools=[self.guideline_lookup],
            llm=self.llm,
            verbose=True
        )
        
        # Care Coordinator Agent
        agents['care_coordinator'] = Agent(
            role=self.agents_config['care_coordinator']['role'],
            goal=self.agents_config['care_coordinator']['goal'],
            backstory=self.agents_config['care_coordinator']['backstory'],
            llm=self.llm,
            verbose=True
        )
        
        return agents
    
    def create_tasks(self, agents, patient_data):
        """Create tasks from YAML configuration"""
        tasks = []
        
        # Symptom Analysis Task
        symptom_task = Task(name="Symptom Analysis Task",
            description=self.tasks_config['symptom_analysis_task']['description'].format(
                patient_info=patient_data['patient_info'],
                symptoms=patient_data['symptoms'],
                medical_history=patient_data['medical_history']
            ),
            expected_output=self.tasks_config['symptom_analysis_task']['expected_output'],
            agent=agents['symptom_analyzer'],
            tools=[self.symptom_checker]
        )
        tasks.append(symptom_task)
        
        # Diagnostic Refinement Task
        diagnostic_task = Task(name="Diagnostic Refinement Task",
            description=self.tasks_config['diagnostic_refinement_task']['description'].format(
                patient_info=patient_data['patient_info'],
                symptom_analysis="{symptom_analysis}"
            ),
            expected_output=self.tasks_config['diagnostic_refinement_task']['expected_output'],
            agent=agents['diagnostic_specialist'],
            context=[symptom_task],
            tools=[self.guideline_lookup]
        )
        tasks.append(diagnostic_task)
        
        # Treatment Recommendation Task
        treatment_task = Task(name="Treatment Recommendation Task",
            description=self.tasks_config['treatment_recommendation_task']['description'].format(
                patient_info=patient_data['patient_info'],
                diagnostic_assessment="{diagnostic_assessment}"
            ),
            expected_output=self.tasks_config['treatment_recommendation_task']['expected_output'],
            agent=agents['treatment_advisor'],
            context=[diagnostic_task],
            tools=[self.guideline_lookup]
        )
        tasks.append(treatment_task)
        
        # Care Coordination Task
        care_task = Task(name="Care Coordination Task",
            description=self.tasks_config['care_coordination_task']['description'].format(
                patient_info=patient_data['patient_info'],
                treatment_plan="{treatment_plan}",
                diagnostic_assessment="{diagnostic_assessment}"
            ),
            expected_output=self.tasks_config['care_coordination_task']['expected_output'],
            agent=agents['care_coordinator'],
            context=[treatment_task]
        )
        tasks.append(care_task)
        
        return tasks
    
    def run_diagnostic_crew(self, patient_data):
        """Run the complete healthcare diagnostic workflow"""
        
        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, patient_data)
        
        # Form the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the workflow
        result = crew.kickoff()
        return result