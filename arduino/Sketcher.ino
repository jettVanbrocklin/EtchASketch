// 58.5 mm = 200 steps = 1 revolution
//3.5 steps per mm
//7 steps per 2mm


#define dirPin1 2
#define stepPin1 3
#define dirPin2 9
#define stepPin2 10
#define stepsPerRevolution 3200



#define M1_M2_M3_MS 16

bool first = true;


void moveXY(int newX, int curX, int newY, int curY){
  int max_steps;

  int diffX = newX - curX;
  int diffY = newY - curY;



  if (diffX >= 0) digitalWrite(dirPin1, LOW);
  else digitalWrite(dirPin1, HIGH);

  if (diffY >= 0) digitalWrite(dirPin2, HIGH);
  else digitalWrite(dirPin2, LOW);


  int num_of_steps_x = int(abs(diffX) * 28);
  int num_of_steps_y = int(abs(diffY) * 28);
  if(num_of_steps_x >= num_of_steps_y) max_steps = num_of_steps_x;
  else max_steps = num_of_steps_y;
    for (int i = 0; i < max_steps; i++){

    if(i < num_of_steps_x){
      digitalWrite(stepPin1, HIGH);
    }
    if(i < num_of_steps_y){
      digitalWrite(stepPin2, HIGH);
    }
    delayMicroseconds(500);
    digitalWrite(stepPin1, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(500);
  }
}



void setup() {

  Serial.begin(9600);
  // Declare pins as output:
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);

  delay(5000);
}

int prev_x;
int prev_y;

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int commaIndex = input.indexOf(',');
    if(first){
      prev_x = 0;
      prev_y = 0;
      first = false;
    }
    if (commaIndex > 0) {
      int x = input.substring(0, commaIndex).toInt();
      int y = input.substring(commaIndex + 1).toInt();
      
      // Use x and y however you'd like
      moveXY(x, prev_x, y, prev_y);
      delay(50);
      prev_x = x;
      prev_y = y;
  }
  // delay(5000);
  // moveXY(330,0,250,0);
  // delay(5000);
  // return;
  }
}
