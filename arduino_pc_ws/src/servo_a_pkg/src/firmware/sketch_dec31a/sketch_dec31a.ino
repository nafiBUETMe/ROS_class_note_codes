#include <Servo.h>
#include <ros.h>
#include<std_msgs/String.h>

#define servo_pin 12

Servo myservo;
int command;

// for command in and out from/to pc
String in_cmd;
String out_cmd;

ros::NodeHandle nh;
std_msgs::String str_msg;

void head_data_in(const std_msgs::String& rec_msg)    //  topic e kono value publish hole, arduino theke ei function ta call hobe
{
  in_cmd = rec_msg.data;          //  topic theke data arduino te ashche in_cmd te 
}

ros::Subscriber<std_msgs::String> ard_sub_head("pc_to_arduino", &head_data_in);

void setup()
{
  Serial.begin(57600);  // baud rate for rosserial
  pinMode(servo_pin,OUTPUT);

  nh.initNode();
  nh.subscribe(ard_sub_head);


}

void loop()
{
  if (in_cmd.length() > 0) {
    if (in_cmd[0] == 'c') { // 'c' for clockwise
      command = in_cmd.substring(1).toInt();
      myservo.write(command);
    } else if (in_cmd[0] == 'a') { // 'a' for anticlockwise
      command = in_cmd.substring(1).toInt();
      myservo.write(-command);
    }
  }
}