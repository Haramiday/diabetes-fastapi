from typing import Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
# İgnore Warnings
import warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
import pickle
cwd = os.getcwd()
file_name = cwd+"/model_d.pkl"


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    
    return {"Hello": "World"}


@app.post("/predict")
async def get_prediction(request: Request):
    # load
    model_loaded = pickle.load(open(file_name, "rb"))
    
    message = await request.json()
    category = {"gender":["Female","Male"],"hypertension":["No","Yes"],"heart_disease":["No","Yes"],
                "smoking_history":['never', 'No Info', 'current', 'former', 'ever', 'not current']}
    #print(category["gender"].index(message["gender"]))
    data = [[category["gender"].index(message["gender"]), message["age"], 
              category["hypertension"].index(message["hypertension"]), category["heart_disease"].index(message["heart_disease"]),
              category["smoking_history"].index(message["smoking_history"]),message["bmi"],message["HbA1c_level"],
              message["blood_glucose_level"]]]
    prediction = model_loaded.predict(data)[0]
    if message["HbA1c_level"]>=5.7:
        result = {"response":"YES"}
    elif (category["hypertension"].index(message["hypertension"])=='Yes' or category["heart_disease"].index(message["heart_disease"])=='Yes') and (category["hypertension"].index(message["hypertension"])=='Yes' and category["heart_disease"].index(message["heart_disease"])=='Yes') and (category["smoking_history"].index(message["smoking_history"])=='current' or category["smoking_history"].index(message["smoking_history"])=='former') and message["blood_glucose_level"]>= 125 and message["bmi"]>= 25:
        result = {"response":"YES"}
    elif category["hypertension"].index(message["hypertension"])=='Yes' and category["heart_disease"].index(message["heart_disease"])=='Yes' and (category["smoking_history"].index(message["smoking_history"])=='current' or category["smoking_history"].index(message["smoking_history"])=='former'):
        result = {"response":"YES"}
    elif category["hypertension"].index(message["hypertension"])=='Yes' and category["heart_disease"].index(message["heart_disease"])=='Yes':
        result = {"response":"YES"}
    elif prediction == 0:
        result = {"response":"NO"}
    else:
        result = {"response":"YES"}
    return result #await request.json()
