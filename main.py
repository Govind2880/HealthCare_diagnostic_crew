from crew import HealthcareDiagnosticCrew


def main(): 
    
    # Sample patient data
    patient_data = {
        'patient_info': '45-year-old male, non-smoker, occasional alcohol',
        'symptoms': 'Persistent headache for 3 days, blurred vision, nausea',
        'medical_history': 'Mild hypertension, family history of migraines'
    }
    
    healthcare_crew = HealthcareDiagnosticCrew()
    
    print("🚀 Starting Healthcare Diagnostic Crew...")
    print("=" * 60)
    
    try:
        result = healthcare_crew.run_diagnostic_crew(patient_data)
        
        print("\n" + "=" * 60)
        print("✅ HEALTHCARE DIAGNOSTIC REPORT COMPLETE")
        print("=" * 60)
        print(result)
        
    except Exception as e:
        print(f"❌ Error running healthcare crew: {e}")

if __name__ == "__main__":
    main()