#include <Servo.h> 
Servo myservo1;  
Servo myservo2;
Servo myservo3;  
Servo myservo4;
void setup() 
{ 
  myservo1.attach(2); 
  myservo2.attach(6); 
  myservo3.attach(9); 
  myservo4.attach(12); 
} 

void loop() 
{ 
  //每个位置休眠1.2秒
  myservo1.write(110);   
  myservo2.write(90);
  myservo3.write(90);   
  myservo4.write(180); 
  delay(1200);

  myservo1.write(90);   
  myservo2.write(50);
  myservo3.write(160);   
  myservo4.write(90); 
  delay(1200);
  
  myservo1.write(160);   
  myservo2.write(90);
  myservo3.write(90);   
  myservo4.write(70); 
  delay(1200);
} 
