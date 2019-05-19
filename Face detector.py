import cv2
import time
import threading
import simpleaudio as sa

#Editable variables

move_variable = 5 #We recomend making the value higher for lower distances from camera and the other way around...

#DON'T TOUCH ANYTHING AFTER THIS COMMENT! or do. i don't care lol...
lastfaces = 0
killthread = False
def sentryscan():
    while killthread == False:
        sentrysound = sa.WaveObject.from_wave_file("sentry_scan.wav")
        sentryobj = sentrysound.play()
        time.sleep(2.5)

cap = cv2.VideoCapture(1)
cap.set(3, 640) #WIDHT
cap.set(4, 480) #HEIGHT
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, -8)

face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar/haarcascade_profileface.xml')

thread = threading.Thread(target=sentryscan)
thread.start()

while(True):


    # Capture frame-by-frame
    ret, frame = cap.read()

    #Detecting the faces from a B&W image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > lastfaces:
        wave_obj = sa.WaveObject.from_wave_file("sentry_spot.wav")
        play_obj = wave_obj.play()
    lastfaces = len(faces)    
    if(len(faces) > 0):
      
        #Opening the files
        xfile = open("X.txt","w")
        yfile = open("Y.txt","w")

        #Handling the X axis
        if((faces[0])[0]+ ((faces[0])[2]/2) - 320 > 150 and (faces[0])[0]+ ((faces[0])[2]/2) - 320 > 0):
            xfile.write(str(-10))
        elif((faces[0])[0]+ ((faces[0])[2]/2) - 320 < -150 and (faces[0])[0]+ ((faces[0])[2]/2) - 320 < 0):
            xfile.write(str(10))

        #Handling the Y axis   
        if((faces[0])[1]+ ((faces[0])[3]/2) - 240 < -100 and (faces[0])[1]+ ((faces[0])[3]/2) - 240 < 0):
            yfile.write(str(-10))
        elif((faces[0])[1]+ ((faces[0])[3]/2) - 240 > 100 and (faces[0])[1]+ ((faces[0])[3]/2) - 240 > 0):
            yfile.write(str(10))

        #Closing the files    
        xfile.close()
        yfile.close()    
    else:

        #If no face is detected set the files to a ignored value
        xfile = open("X.txt","w")
        yfile = open("Y.txt","w")
        xfile.write(str(2019))
        yfile.write(str(2019))
        xfile.close()
        yfile.close()
        
        xfile.close()

    #Displaying the resulting frame
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
             cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.rectangle(frame,(320-150,240-100),(320+150, 240+100),(0,255,0),2)
    cv2.imshow('frame',frame)

    #Killing the program on Q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        killthread = True
        break
        
