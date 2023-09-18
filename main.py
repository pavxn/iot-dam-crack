"""
TODO
run a script that collects analog from flex sensors
store it in mongodb, and retrieve it 
als
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib, json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/')
async def get_predictions(val : Request):
    print(val)
    val = await val.json()
    values = list(val.values())
    res = predict(values)
    print(res)
    if res:
        final_res = {
            'z1' : values[0],
            'z2' : values[1],
            'z3' : values[2],
            'pred' : res
        }

        return final_res
    

def predict(values):
    file = open('./lm_model.pkl', 'rb')
    model = joblib.load(file)
    res = model.predict([values])[0]
    file.close()
    return res
