#控制一个舵机锁定人脸初版，对应ino为ctrl1servo
import face_recognition
import cv2
import time
import threading
import serial

#这个是摄像头的宽度分辨率
framewidth= 640     
#注意串口号对应                
ser = serial.Serial('COM5', 9600) 
#摄像头张角45度，那么中间的位置就是23度
s=23
slast=23

class MyThread(threading.Thread):
    def __init__(self, func, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func

    def run(self):
        if self.name == "send":
            matter1()
        elif self.name == "change":
            matter2()

def matter1():
    while True:
        global s
        global slast
        #识别发现位置有变化时发送转动指令
        if(s!=slast):
            ser.write(bytes(str(s), encoding="utf8"))
            print(s)
        slast=s
        #两秒内只发送一次，避免机械臂停不下来的问题
        time.sleep(2)

def matter2():
    global s
    video_capture = cv2.VideoCapture(0)

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

    num = 0
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        process_this_frame = not process_this_frame
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            #s定位是现在人脸的位置
            s = int((left + right - 1) /framewidth * 45 / 2)
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"        
            for i in range(len(known_face_names)):
                if matches[i]:name = known_face_names[i]
                else:pass
            
            cv2.putText(frame, "cam", (50,100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
            num = num + 1
            filename = "output/frames_%s.jpg" % num
            cv2.imwrite(filename, frame)
                    
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #一个线程发送控制信号，一个线程专门做识别
    thing1 = MyThread(matter1,"send")
    thing2 = MyThread(matter2,"change")
    thing1.start()
    thing2.start()
    thing1.join()
    thing2.join()
    #断开连接
    ser.close()