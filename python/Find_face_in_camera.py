#从摄像头中找到人脸,参考facerec_from_webcam_faster.py
#实时播放出来，打水印并把截图保存下来
import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

#找这些人脸
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
lijiawei_image = face_recognition.load_image_file("lijiawei.jpg")
lijiawei_face_encoding = face_recognition.face_encodings(lijiawei_image)[0]
known_face_encodings = [
    obama_face_encoding,
    lijiawei_face_encoding]
known_face_names = [
    "Obama",
    "lijiawei"]

#num用来为存储的截图计数命名
num = 0
#process_this_frame确定这一帧是否进行识别
process_this_frame = True
while True:
    #切片得到一张截图
    ret, frame = video_capture.read()
    
    #在这里把视频缩放到只有1/4*1/4，调整RGB
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    #隔一帧做一次识别
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    process_this_frame = not process_this_frame
    
    #呈现与保存
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #将缩放还原
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        #找人名
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"        
        for i in range(len(known_face_names)):
            if matches[i]:name = known_face_names[i]
            else:pass
        
        #打水印保存截图
        cv2.putText(frame, "cam", (50,100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
        num = num + 1
        filename = "output/frames_%s.jpg" % num
        cv2.imwrite(filename, frame)
                  
        #实时展示画个框把脸框起来，画个标签框里面写上找到的人的名字
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
    #实时展示
    cv2.imshow('Video', frame)

    #Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#Release
video_capture.release()
cv2.destroyAllWindows()
