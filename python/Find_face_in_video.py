#从视频中找到人脸,可以参考example/facerec_from_video_file.py，它是整体输出到output.avi里。
#这里我实时播放出来，并把截图保存下来
import face_recognition
import cv2

#在这个视频里识别人脸
video_capture = cv2.VideoCapture("hamilton_clip.mp4")

#找这个人脸
obama_image = face_recognition.load_image_file("lin-manuel-miranda.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

#num用来为存储的截图计数命名
num = 0
while True:
    #切片得到一张截图
    ret, frame = video_capture.read()

    #这个地方注意CV2颜色顺序的一个坑，他是BGR，这里转成RGB
    rgb_frame = frame[:, :, ::-1]

    #找人脸
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    #在找到的人脸旁做标注
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        match = face_recognition.compare_faces([obama_face_encoding], face_encoding)

        name = "Unknown"
        if match[0]:
            name = "miranda"

        #在截图上打个标签，先写人名吧，表示处理过，将来可扩展处理方式
        cv2.putText(frame, name, (50, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        #把截图存下来,要建一下output文件夹不然报错找不到路径
        num = num + 1
        filename = "output\\frames_%s.jpg" % num
        cv2.imwrite(filename, frame)

        #画个框把脸框起来
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #画个标签框里面写上找到的人的名字
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