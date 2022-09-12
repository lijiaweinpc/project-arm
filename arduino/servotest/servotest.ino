#include <Servo.h> 
Servo myservo;  
//初始位置为先到0
int pos = 0;     
void setup() 
{
  //setup里只执行一次；舵机连接到1号位。
  myservo.attach(1);  
} 

void loop() 
{
  //正反转180度
  for(pos = 0; pos <= 180; pos += 1) 
  {                                  
    myservo.write(pos);     
    //1度20ms              
    delay(20);
  }
  for(pos = 180; pos>=0; pos-=1)   
  {                                
    myservo.write(pos);              
    delay(20);                  
  } 
} 
