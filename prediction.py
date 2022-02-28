from keras.models import model_from_json
import numpy as np
import operator
import cv2

json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)
loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

uscore=0
cscore=0

cap = cv2.VideoCapture(0) 

categories = {0: 'Stone', 1: 'wi1', 2: 'Scissor', 3: 'wi3', 4: 'wi4', 5: 'Paper'}

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])

    cv2.putText(frame, "Stone-Paper-Scissor", (175, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (225,255,0), 3)
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,255,255) ,3)
    roi = frame[y1:y2, x1:x2]

    roi = cv2.resize(roi, (64, 64)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    cv2.putText(frame, "R.O.I", (440, 350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,225,0), 3)

    _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", test_image)

    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
    prediction = {'STONE': result[0][0], 
                  'ONE': result[0][1], 
                  'PAPER': result[0][2],
                  'THREE': result[0][3],
                  'FOUR': result[0][4],
                  'SCISSOR': result[0][5]}
    moves=['STONE','PAPER','SCISSOR']
    t=np.random.randint(0,3)
    computer=moves[t]
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True) 
    user=prediction[0][0]
    flag=0
    if user=='ONE' or user=='THREE' or user=='FOUR':
        cv2.putText(frame, "WRONG INPUT", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        flag=1
        cv2.imshow("Frame", frame)

    if computer=='STONE' and user=='PAPER':
        uscore+=1
    elif computer=='STONE' and user=='SCISSOR':
        cscore+=1
    elif computer=='PAPER' and user=='STONE':
        cscore+=1
    elif computer=='PAPER' and user=='SCISSOR':
        uscore+=1
    elif computer=='SCISSOR' and user=='PAPER':
        cscore+=1
    elif computer=='SCISSOR' and user=='STONE':
        uscore+=1
    
    if flag ==0:
        cv2.putText(frame, "USER:"+str(uscore), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, prediction[0][0], (80, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)    
        cv2.putText(frame, "COMPUTER:"+str(cscore), (30, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, computer, (80, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)    
        cv2.imshow("Frame", frame)

    if(uscore>=5):
         cv2.putText(frame, "USER WON!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
         cv2.waitKey(1000)

    if(cscore>=5):
         cv2.putText(frame, "COMPUTER WON!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
         cv2.waitKey(1000)

    interrupt = cv2.waitKey(50)
    if interrupt & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()