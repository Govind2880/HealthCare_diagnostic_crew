from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class SymptomCheckerInput(BaseModel):
    symptoms: str = Field(..., description="Patient symptoms to check")
    age: int = Field(..., description="Patient age")
    gender: str = Field(..., description="Patient gender")


class SymptomCheckerTool(BaseTool):
    name: str = "symptom_checker"
    description: str = "Checks symptoms and provides basic medical information"
    args_schema: Type[BaseModel] = SymptomCheckerInput

    def _run(self, symptoms: str, age: int, gender: str) -> str:
        # This is a simplified version - in real implementation, 
        # you would integrate with medical databases or APIs
        return f"""
        Symptom Analysis for {age}-year-old {gender}:
        Symptoms: {symptoms}
        
        Basic Assessment:
        - Symptoms categorized and analyzed
        - Common conditions considered based on age and gender
        - General recommendations provided
        
        Note: This is preliminary analysis and should be verified by healthcare professionals.
        """


class MedicalGuidelineInput(BaseModel):
    condition: str = Field(..., description="Medical condition to check guidelines for")


class MedicalGuidelineTool(BaseTool):
    name: str = "medical_guideline_lookup"
    description: str = "Looks up current medical guidelines for specific conditions"
    args_schema: Type[BaseModel] = MedicalGuidelineInput

    def _run(self, condition: str) -> str:
        # Mock implementation - in real scenario, connect to medical databases
        guidelines = {
            "hypertension": "Lifestyle modifications + consider medication if BP > 130/80",
            "diabetes": "Monitor blood sugar, dietary control, exercise, medication as needed",
            "asthma": "Inhaled corticosteroids for maintenance, rescue inhalers for acute symptoms",
            "migraine": "Acute treatment + preventive medications for frequent episodes"
        }
        return guidelines.get(condition.lower(), "Consult current medical guidelines for specific recommendations")