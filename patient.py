from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for validation
class Patient(BaseModel):
    id: int
    name: str
    age: int

# In-memory storage
patients: List[Patient] = [
    Patient(id=1, name="John Doe", age=40),
    Patient(id=2, name="Jane Smith", age=35),
]

# Get all patients
@app.get("/patients", response_model=List[Patient])
def get_patients():
    return patients

# Get patient by ID
@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Add new patient
@app.post("/patients", response_model=Patient, status_code=201)
def add_patient(patient: Patient):
    patients.append(patient)
    return patient

# Update patient
@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            patients[index] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Delete patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            patients.remove(patient)
            return {"message": "Patient deleted"}
    raise HTTPException(status_code=404, detail="Patient not found")

# To run:
# uvicorn patient:app --reload