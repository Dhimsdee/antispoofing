# USAGE
# python test.py --model liveness.model --le le.pickle --detector face_detector

from imutils.video import VideoStream
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os

# Uncomment argument di bawah jika ingin menjalankan melalui terminal
""" ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", type=str, required=True,
        help="path to trained model")
ap.add_argument("-l", "--le", type=str, required=True,
        help="path to label encoder")
ap.add_argument("-d", "--detector", type=str, required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args()) """

def livenessnet(model_Path, le_path, detector_folder, confidence=0.5):
    args = {'model':model_Path, 'le':le_path, 'detector':detector_folder, 'confidence':confidence}

    # load the serialized face detector from disk
    print("Loading face detector...")
    protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
    modelPath = os.path.sep.join([args["detector"],
        "res10_300x300_ssd_iter_140000.caffemodel"])
    net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # load the liveness detector model and label encoder from disk
    print("Loading Model...")
    model = load_model(args["model"])
    le = pickle.loads(open(args["le"], "rb").read())

    # initialize the video stream and allow camera to warmup
    print("Starting Video Stream")
    v = VideoStream(src=0).start()
    time.sleep(2.0) # wait for the camera to warmup
    # count the sequence that person appears
    sequence_count = 0

    # initialize variables needed to return
    # in case, users press 'q' before the program process the frame
    label = 'fake'

    # iterate over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to 600 pixels
        frame = v.read()
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]

        # grab the frame dimensions and convert it to a blob
        # blob is used to preprocess image to be easy to read for NN
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                    (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network then obtain the detections and predictions
        net.setInput(blob)
        detections = net.forward()

        # iterate over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e. probability) associated with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > args["confidence"]:
                # compute the (x,y) coordinates of the bounding box
                # for the face and extract the face ROI
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # expand the bounding box a bit
                # (from experiment, the model works better this way)
                # and ensure that the bounding box does not fall outside of the frame
                startX = max(0, startX-20)
                startY = max(0, startY-20)
                endX = min(w, endX+20)
                endY = min(h, endY+20)

                # extract the face ROI and then preprocess it
                # in the same manner as our training data
                face = frame[startY:endY, startX:endX] # for liveness detection
                face = cv2.resize(face, (32, 32))
                face = face.astype("float") / 255.0
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)

                # pass the face ROI through the trained liveness detection model
                # to determine if the face is 'real' or 'fake'
                preds = model.predict(face)[0]
                j = np.argmax(preds)
                label = le.classes_[j]  # get label of predicted class

                # draw the label and bounding box on the frame
                # label = "{}: {:.4f}".format(label, preds[j])
                print(label)

                if preds[j] > 0.60 and j == 1:
                    sequence_count += 1
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    _label = "Real: {:.4f}".format(preds[j])
                    # cv2.putText(frame, _label, (startX, startY - 10),
                    #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                else:
                    sequence_count += 1
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    _label = "Fake/Spoofed: {:.4f}".format(preds[j])
                    # cv2.putText(frame, _label, (startX, startY - 10),
                    #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the output fame and wait for a key press
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if 'q' is pressed, stop the loop
        # if the person appears 40 frames in a row, stop the loop
        if key == ord("q") or sequence_count==40:
            break

    cv2.destroyAllWindows()
    v.stop()

    time.sleep(2)
    return label

if __name__ == '__main__':
    label = livenessnet('LivenessNet.model', 'le.pickle', 'face_detector', confidence=0.5)
    print(label)