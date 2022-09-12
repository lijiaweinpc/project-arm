#include <Servo.h> 
Servo myservo;
//起始位置设为中间
int pos = 90;   
//用poslast记录上一个指令位置，也就是当前的位置
int poslast = 90;
//控制命令初值h(hold)，保持不变
char now = 'h';   
void setup() 
{
  Serial.begin(9600);  
  myservo.attach(9);
  myservo.write(pos);
}

void loop() 
{
  //把当前的位置记录下来，用pos去接下一个控制指令
  poslast = pos;
  switch(now)
  {
    //left减10度，right加10度
    case 'l':pos -= 10;break;
    case 'r':pos += 10;break;
    default:break;
  }
  //位置限制到0和180之间
  pos = constrain(pos,0,180);
  now = 'h';
  //当pos与poslast不等位置需要改变时
  if(!(pos == poslast))
  {
    //运动，给50ms时间
    myservo.write(pos);
    delay(50);
  }
  if (Serial.available() > 0) 
  {
    // 读取下一个命令
    now = Serial.read();
  }
}
