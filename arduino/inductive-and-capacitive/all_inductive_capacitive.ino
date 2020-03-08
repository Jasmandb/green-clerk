int ind_1, ind_2, ind_3, ind_4, ind_5, ind_6 = HIGH;
int cap_1, cap_2, cap_3, cap_4, cap_5, cap_6 = HIGH;
int temp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //6 inductive sensors
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  //6 capacitive sensors
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //inductive sensor reads
  temp = digitalRead(2);
  if (temp != ind_1)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 1 is detecting an object");
    }
    ind_1 = temp;
  }
  temp = digitalRead(3);
  if (temp != ind_2)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 2 is detecting an object");
    }
    ind_2 = temp;
  }
  temp = digitalRead(4);
  if (temp != ind_3)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 3 is detecting an object");
    }
    ind_3 = temp;
  }
  temp = digitalRead(5);
  if (temp != ind_4)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 4 is detecting an object");
    }
    ind_4 = temp;
  }
  temp = digitalRead(6);
  if (temp != ind_5)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 5 is detecting an object");
    }
    ind_5 = temp;
  }
  temp = digitalRead(7);
  if (temp != ind_6)
  {
    if (temp == LOW)
    {
      Serial.println("Inductive Sensor # 6 is detecting an object");
    }
    ind_6 = temp;
  }
  //capacitive sensor reads
  temp = digitalRead(8);
  if (temp != cap_1)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 1 is detecting an object");
    }
    cap_1 = temp;
  }
  temp = digitalRead(9);
  if (temp != cap_2)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 2 is detecting an object");
    }
    cap_2 = temp;
  }
  temp = digitalRead(10);
  if (temp != cap_3)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 3 is detecting an object");
    }
    cap_3 = temp;
  }
  temp = digitalRead(11);
  if (temp != cap_4)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 4 is detecting an object");
    }
    cap_4 = temp;
  }
  temp = digitalRead(12);
  if (temp != cap_5)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 5 is detecting an object");
    }
    cap_5 = temp;
  }
  temp = digitalRead(13);
  if (temp != cap_6)
  {
    if (temp == LOW)
    {
      Serial.println("Capacitive Sensor # 6 is detecting an object");
    }
    cap_6 = temp;
  }
}
