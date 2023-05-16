

import numpy as np
import cv2
# from keras.backend.cntk_backend import clear_session
from keras.preprocessing import image

# -----------------------------
# opencv initialization
from src.dbconnection import iud, iud1

face_cascade = cv2.CascadeClassifier('static/model/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
# -----------------------------
# face expression recognizer initialization
from keras.models import model_from_json


print("==========================")
# clear_session()

model = model_from_json(open("static/model/facial_expression_model_structure.json", "r").read())
model.load_weights('static/model/facial_expression_model_weights.h5')  # load weights

# -----------------------------

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')



cascPath = "static/model/haarcascade_frontalface_default.xml"
# def emotioncheck(fn):
#
#     # while(True):
#     # ret, img = cap.read()
#     print(fn,"=============================")
#     img = cv2.imread('sample.png')
#
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     faceCascade = cv2.CascadeClassifier(cascPath)
#
#     faces = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30),
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )
#     # print(faces) #locations of detected faces
#     print("jiiiiii------------", faces)
#     for (x, y, w, h) in faces:
#         print("face-----------------")
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draw rectangle to main image
#
#         detected_face = img[int(y):int(y + h), int(x):int(x + w)]  # crop detected face
#         detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # transform to gray scale
#         detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48
#
#         img_pixels = image.img_to_array(detected_face)
#         img_pixels = np.expand_dims(img_pixels, axis=0)
#         img_pixels /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
#
#         predictions = model.predict(img_pixels)  # store probabilities of 7 expressions
#
#         # find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
#         max_index = np.argmax(predictions[0])
#
#         emotion = emotions[max_index]
#
#         # write emotion text above rectangle
#         # cv2.putText(img, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
#         print("---------------", emotion)
#         if emotion is not None:
#             return emotion
#         else:
#             return "neutral"

    # process on detected face end
    # -------------------------


#
# import numpy as np
# import argparse
# # import imutils
# import time
# import cv2
# import os
#
# # labelsPath = os.path.sep.join([r"mainfn","coco.names"])
#
#
#
#
#
# # LABELS = open(labelsPath).read().strip().split("\n")
#
# # initialize a list of colors to represent each possible class label
# # np.random.seed(42)
# # COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
# # 	dtype="uint8")
# #
# # # derive the paths to the YOLO weights and model configuration
# # weightsPath = os.path.sep.join([r"mainfn", "model.weights"])
# # configPath = os.path.sep.join([r"mainfn", "model.cfg"])
# #
# # # load our YOLO object detector trained on COCO dataset (80 classes)
# # # and determine only the *output* layer names that we need from YOLO
# # print("[INFO] loading YOLO from disk...")
# # net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# # ln = net.getLayerNames()
# # ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

import cv2
import imutils

video_capture = cv2.VideoCapture(0)
i = 0
while True:
    ret, frame = video_capture.read()
    cv2.imwrite("sample1.png", frame)
    import datetime
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    cv2.imwrite("static/imgg/"+str(date)+'.jpg', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cascPath)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # print(faces) #locations of detected faces
    print("jiiiiii------------", faces)

    for (x, y, w, h) in faces:
        print("face-----------------")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draw rectangle to main image

        detected_face = frame[int(y):int(y + h), int(x):int(x + w)]  # crop detected face
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # transform to gray scale
        detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48

        img_pixels = image.img_to_array(detected_face)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

        predictions = model.predict(img_pixels)  # store probabilities of 7 expressions

        # find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
        max_index = np.argmax(predictions[0])

        emotion = emotions[max_index]

        # write emotion text above rectangle
        cv2.putText(frame, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        print("---------------", emotion)

        # cv2.imread('a.jpg', frame)

        print(i,"count")
        i = i+1



        # print("count",i)
        if i == 20:


            q="UPDATE `customer_emotion` SET `status`='notified'"
            iud1(q)
            qry="INSERT INTO `customer_emotion` (`cam_id`,`emotions`,`date`,image,status)  VALUES (%s,%s,CURDATE(),%s,'pending')"
            iud(qry,(1,emotion,date+'.jpg'))
            i = 0
        #
        # # return emotion
        # i = i + 1

    cv2.imshow('image', frame)  # Display video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#
# # Release capture
# video_capture.release()
# cv2.destroyAllWindows()

