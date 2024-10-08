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
    data = [[category["gender"].index(message["gender"]), int(message["age"]), 
              category["hypertension"].index(message["hypertension"]), category["heart_disease"].index(message["heart_disease"]),
              category["smoking_history"].index(message["smoking_history"]),float(message["bmi"]),float(message["HbA1c_level"]),
              int(message["blood_glucose_level"])]]
    prediction = model_loaded.predict(data)[0]
    if float(message["HbA1c_level"])>=5.7:
        result = {"response":"YES"}
    elif (message["hypertension"]=='Yes' or message["heart_disease"]=='Yes') and (message["smoking_history"]=='current' or message["smoking_history"]=='former') and int(message["blood_glucose_level"])>= 125 and float(message["bmi"])>= 25 and float(message["HbA1c_level"])>=5.7:
        result = {"response":"YES"}
    elif message["hypertension"]=='Yes' and message["heart_disease"]=='Yes' and (message["smoking_history"]=='current' or message["smoking_history"]=='former'):
        result = {"response":"YES"}
    elif message["hypertension"]=='Yes' and message["heart_disease"]=='Yes':
        result = {"response":"YES"}
    elif prediction == 0:
        result = {"response":"NO"}
    else:
        result = {"response":"NO"}
    return result #await request.json()
