'''
TODO
1. write wrapper code that scans every document, seperates the sens_id, and calculates risk
2. if significant risk (change within a short amount of time), look at adjacent nodes too, and their risk score
3. compile and output a risk score directly, or feed into an ML model, with left, center and right vals, and get a risk eval.

Statitical Model:
For every sensor, calculate z-score of latest value
This identifies spike in latest data.
Retrieve max z-score out of all sensors, retrieve left and right values, and give final score.
'''

import time
import pymongo
from pydantic import BaseModel
import statistics as st
import requests

class Val(BaseModel):
    id : int
    left : int
    right : int
    time : str
    value : int

def getDocs():
    client = pymongo.MongoClient("mongodb+srv://pavan:pavan@iot1.yjorxvt.mongodb.net/?retryWrites=true&w=majority")
    col = client.iot.data
    docs = col.find()    
    res = []
    for doc in docs:
        res.append(doc)

    return res

def run():
    global sens_ids, sens_sep, url
    temp = getDocs()
    temp1 = temp
    res = []
    sens_ids = []
    for doc in temp:
        res.append(Val(**doc))
        

    for doc in res:
        if doc.id not in sens_ids:
            sens_ids.append(doc.id)

    sens_sep = {}
    for id in sens_ids:
        temp = []
        for doc in res:
            if id == doc.id:
                temp.append(doc)
        sens_sep[id] = temp

    url = 'https://iotbackend-pavanapril14.b4a.run/'
    print(sens_ids)


def getMaxRisk():
    run()
    z_scores = {}
    for sens in sens_ids:
        z_scores[sens] = abs(getZVal(sens))
    print(z_scores)
      
    # get sensor with max z-score, and their left and right nodes
    sens_id = max(z_scores, key= lambda x: z_scores[x])

    left, right = sens_sep[sens_id][0].left, sens_sep[sens_id][0].right
    print(left, sens_id, right)
    z_max = max(z_scores.values())
    z_left, z_right = abs(getZVal(left)), abs(getZVal(right))

    vals = {
        "z_left" : z_left,
        "z_mid" : z_max,
        "z_right" : z_right
    }

    x = requests.post(url, json=vals)
    
    return [left, z_left, sens_id, z_max, right, z_right, x.json()]


def getZVal(sens_id):
    res = sens_sep[sens_id]
    res.sort(key=lambda x: x.time, reverse=True)
    latest = res[0].value
    values = [i.value for i in res]

    mean = st.mean(values)
    std = st.stdev(values)
    z_score = (latest - mean)/std

    return z_score


while(True):
    left, z_left, sens_id, z_max, right, z_right, pred = getMaxRisk()

    print(f"\n\t\tFlex Sensor Z-SCORES: \n\nHighest spike:\nSensor ID({sens_id})\tSensor-Left({left})\tSensor-Right({right})\n" + f'{z_max:.4f}' + '\t\t' + f'{z_left:.4f}' + '\t\t' + f'{z_right:.4f}')

    print("\nPrediction:\n" + pred['pred'].upper())

    time.sleep(10)
