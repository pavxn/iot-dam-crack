import time, pymongo
import random, serial
client = pymongo.MongoClient("mongodb+srv://pavan:pavan@cluster0.zey2mcj.mongodb.net/?retryWrites=true&w=majority")
col = client.iot.data

serial_port = '/dev/ttyACM0';
baud_rate = 9600;
ser = serial.Serial(serial_port, baud_rate)

def getValue(sens):
    return random.randint(1020, 1023)

def  upload(sens_id, value):
    left, right = sens_id-1, sens_id+1
    values = {
        "id": sens_id,
        "time" : time.time(),
        "value" : value,
        "left" : left,
        "right" : right
    }

    x = col.insert_one(values)
    print("Inserted: ", x.inserted_id)


def sensorValues():
    line = ser.readline().decode()
    #print(line1,line2)
    
    val1, val2 = line.split(',')
    val1, val2 = int(val1), int(val2[:-2])

    print(val1, val2)
    return([val1, val2])



while(True):
    val1, val2 = sensorValues()
    upload(6, val1)
    upload(7, val2)
    time.sleep(1)
    upload(random.randint(4,5), getValue(1))
    time.sleep(1)
    upload(random.randint(8,9), getValue(1))
    
