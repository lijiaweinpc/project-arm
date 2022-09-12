//line存储传入的串行数据
char line[500] = "";  
int ret = 0;
void setup() 
{
  //打开串口，设置数据传输速率9600
  Serial.begin(9600);     
}

void loop() 
{
  // 在串口可用时才读取
  if (Serial.available() > 0) 
  {    
    // 读取数据存入line，读到'\n'为止，或者最多读500个字符
    ret = Serial.readBytesUntil('\n', line, 500);
    //打印读取到的内容：
    Serial.print("serial recevied:");
    Serial.println(line);   
  }
}
