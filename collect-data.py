import cv2
import os

if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/train")
    os.makedirs("data/test")
    os.makedirs("data/train/stone")
    os.makedirs("data/train/wi1")
    os.makedirs("data/train/scissor")
    os.makedirs("data/train/wi3")
    os.makedirs("data/train/wi4")
    os.makedirs("data/train/paper")
    os.makedirs("data/test/stone")
    os.makedirs("data/test/wi1")
    os.makedirs("data/test/scissor")
    os.makedirs("data/test/wi3")
    os.makedirs("data/test/wi4")
    os.makedirs("data/test/paper")

mode = 'train'
directory = 'data/'+mode+'/' 

cap=cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    cv2.putText(frame, "Stone-Paper-Scissor", (175, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (225,255,255), 3)

    count = {'stone': len(os.listdir(directory+"/stone")),
            'wi1': len(os.listdir(directory+"/wi1")),
            'scissor': len(os.listdir(directory+"/scissor")),
            'wi3': len(os.listdir(directory+"/wi3")),
            'wi4': len(os.listdir(directory+"/wi4")),
            'paper': len(os.listdir(directory+"/paper"))}

    cv2.putText(frame, "MODE : "+mode, (30, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (225,255,255), 1)
    cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (225,255,255), 1)
    cv2.putText(frame, "STONE : "+str(count['stone']), (10, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
    cv2.putText(frame, "WRONG INPUT-ONE : "+str(count['wi1']), (10, 140), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
    cv2.putText(frame, "SCISSOR : "+str(count['scissor']), (10, 160), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
    cv2.putText(frame, "WRONG INPUT-THREE : "+str(count['wi3']), (10, 180), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
    cv2.putText(frame, "WRONG INPUT-FOUR : "+str(count['wi4']), (10, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)
    cv2.putText(frame, "PAPER : "+str(count['paper']), (10, 220), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)

    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,3)
    roi = frame[y1:y2, x1:x2]
    roi = cv2.resize(roi, (200, 200))
    cv2.putText(frame, "R.O.I", (440, 350), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,225,0), 3)
    cv2.imshow("Frame", frame)

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", roi)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:
        break
    if interrupt & 0xFF == ord('0'):
        cv2.imwrite(directory+'stone/'+str(count['stone'])+'.jpg', roi)
    if interrupt & 0xFF == ord('1'):
        cv2.imwrite(directory+'wi1/'+str(count['wi1'])+'.jpg', roi)
    if interrupt & 0xFF == ord('2'):
        cv2.imwrite(directory+'scissor/'+str(count['scissor'])+'.jpg', roi)
    if interrupt & 0xFF == ord('3'):
        cv2.imwrite(directory+'wi3/'+str(count['wi3'])+'.jpg', roi)
    if interrupt & 0xFF == ord('4'):
        cv2.imwrite(directory+'wi4/'+str(count['wi4'])+'.jpg', roi)
    if interrupt & 0xFF == ord('5'):
        cv2.imwrite(directory+'paper/'+str(count['paper'])+'.jpg', roi)

cap.release()
cv2.destroyAllWindows()