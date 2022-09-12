#include <Servo.h> 
Servo myservo1;  
Servo myservo2;
Servo myservo3;  
Servo myservo4;
void setup() 
{
  //舵机从上到下依次连接接口2,6,9,12
  myservo1.attach(2); 
  myservo2.attach(6); 
  myservo3.attach(9); 
  myservo4.attach(12); 
  //归中位置（90,50,160,90），休眠位置（120,0,180,90）
  myservo1.write(120);   
  myservo2.write(0);
  myservo3.write(180);   
  myservo4.write(90); 
} 

void loop() 
{ 
} 
