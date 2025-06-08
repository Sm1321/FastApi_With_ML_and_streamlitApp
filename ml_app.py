from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from schema.user_input import UserInput

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

#ML Flow
MODEL_VERSION = "1.0.0"

app = FastAPI()


@app.get('/')
def home():
    return {'messages':'Insurance Preminum Preidiction API'}

#Health API to check , Machine Readable
@app.get('/healthCheck')
def health_check():
    return {
        'status':'OK',
        'Version':MODEL_VERSION,
        'Model_loaded': model is not None
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})




