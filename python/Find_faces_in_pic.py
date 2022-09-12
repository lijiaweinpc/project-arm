#在一张图片里找多个人的人脸，之前测试时发现识别率有待提高，存在较多的误认；
#参考了identify_and_draw_boxes_on_faces.py
#face_recognition可以计算两张照片的相似度，见example/face_distance.py
import face_recognition
import cv2

#在这张frame里的识别人脸
frame = cv2.imread("two_people.jpg")

#识别哪些人脸，每人给一张就可以了
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding]
known_face_names = [
    "Obama",
    "Joe Biden"]

#找到frame中的所有人脸
face_locations = face_recognition.face_locations(frame)
face_encodings = face_recognition.face_encodings(frame, face_locations)
print("I found {} face(s) in this photograph.".format(len(face_locations)))

#在找到的人脸旁边做标注
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"
    #画个框把脸框起来
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    
    #把人名读出来，这里如果排在靠后位置的是个大众脸，那误识可就高了
    for i in range(len(known_face_names)):
        if matches[i]:name = known_face_names[i]
        else:pass
    
    #画个标签框里面写上找到的人的名字
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#输出
cv2.imwrite("find.jpg",frame)