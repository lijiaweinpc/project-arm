#include <Servo.h> 
Servo myservo;  
int pos = 90;
int poslast = 90;
//串口接收角度数据，转int
int nextmove = 0;
char line[100] = "";
void setup() 
{
  Serial.begin(9600); 
  myservo.attach(12);
  myservo.write(pos);
}

void loop() 
{
  poslast = pos;
  if (Serial.available() > 0) 
  {
    nextmove = Serial.readBytesUntil('\n', line, 500);
    nextmove = atoi(line);
    for(int i = 0;i < 5;i++)
    {
      line[i]='\0';
    }
    Serial.println(nextmove);   
    
   //如果人脸中心在15到30度之间的话可以接受，就不用转动了
   if(nextmove > 30)
   {
    for(int i = 0;i < nextmove - 22;i += 1) 
    {
     pos -= 1;
     pos=constrain(pos,0,180);
     if(!(pos == poslast))
     {
      myservo.write(pos);
      delay(20);
     }
    }
   }
   if(nextmove < 15)
   {
    for(int i = 0;i < 23 - nextmove;i += 1) 
    {
     pos += 1;
     pos=constrain(pos,0,180);
     if(!(pos == poslast))
     {
      myservo.write(pos);
      delay(20);
     }
    }
   }
  } 
}
