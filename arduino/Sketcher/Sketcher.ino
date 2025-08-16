// 58.5 mm = 200 steps = 1 revolution
//3.5 steps per mm
//7 steps per 2mm

// 600 steps left to right
// 430 steps up and down


#define dirPin1 2
#define stepPin1 3
#define dirPin2 9
#define stepPin2 10
#define stepsPerRevolution 200


#define M1_M2_M3_MS 1

bool first = true;

// to set up backlash behavior, "true" is high, "false" is low
bool prev_dir_y = true;
bool prev_dir_x = true;

bool cur_dir_y = true;
bool cur_dir_x = true;

void moveXY(int newX, int curX, int newY, int curY){
  int max_steps;

  int diffX = newX - curX;
  int diffY = newY - curY;



  if (diffX >= 0){
    digitalWrite(dirPin1, LOW);
    cur_dir_x = false;
  }
  else{
    digitalWrite(dirPin1, HIGH);
    cur_dir_x = true;
  }
  if (diffY >= 0){
    digitalWrite(dirPin2, HIGH);
    cur_dir_y = true;
  }
  else{
    digitalWrite(dirPin2, LOW);
    cur_dir_y = false;
  }
  delayMicroseconds(200);

  int backlash_offset_x = 0;
  int backlash_offset_y = 0;
  if(cur_dir_x != prev_dir_x) backlash_offset_x = 3 * M1_M2_M3_MS;
  if(cur_dir_y != prev_dir_y) backlash_offset_y = 2 * M1_M2_M3_MS;
  prev_dir_x = cur_dir_x;
  prev_dir_y = cur_dir_y;
  int num_of_steps_x = int(abs(diffX) * 1) + backlash_offset_x;
  int num_of_steps_y = int(abs(diffY) * 1) + backlash_offset_y;


  // int num_of_steps_x = int(abs(diffX) * (20));
  // int num_of_steps_y = int(abs(diffY) * 20);
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
    delay(1);
  }
}



void setup() {

  Serial.begin(9600);
  // Serial.print("Starting...");
  // Declare pins as output:
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);

  delay(5000);
}

int prev_x;
int prev_y;

//////////////// Main
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
      prev_x = x;
      prev_y = y;
  }
  return;
  }
}

// TEST 1, 5 pixels = 1.55, 10 pixels ~ 3.1, Safe to say each pixel is around 


// first test moves etch a sketch to center, and draws 1 pixel to the right, 5 pixels to the right, and 10 pixels to the right
// int num_points = 1;
// int x_values[] = {300};
// int y_values[] = {215};
// int iterator = 0;
// ////////////////// Testing
// void loop() {
//   if(first){
//     prev_x = 0;
//     prev_y = 0;
//   }
//   moveXY(x_values[iterator], prev_x, y_values[iterator], prev_y);
//   Serial.print("Iterator: ");
//   Serial.print(iterator);
//   Serial.print("\n");
//   if(first){
//     delay(3000);
//     first = false;
//   }
//   prev_x = x_values[iterator];
//   prev_y = y_values[iterator];
//   iterator++;
//   if(iterator >= 6){
//     delay(100000);
//   }
//   delay(1000);
// }

//TEST 2, CHECKING RESOLUTION, AND IN TURN GETTING STEP TO PIXEL RATIO

// void loop(){

//   digitalWrite(dirPin2, HIGH);
//   delayMicroseconds(100);


//   // Spin the stepper motor 1 revolution slowly:
//   int step = 0;
//   while(1) {
//     // These four lines result in 1 step:
//     digitalWrite(stepPin2, HIGH);
//     delayMicroseconds(500);
//     digitalWrite(stepPin2, LOW);
//     delayMicroseconds(500);

//     step ++;

//     Serial.print("Current Step: ");
//     Serial.print(step);
//     Serial.print("\n");

//     delay(10);

//   }

// }

