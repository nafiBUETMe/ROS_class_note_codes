#include <ros.h> //for ros serial communication
#include <std_msgs/String.h> //for ros serial communication

#define servo_pin_x 12//

String in_cmd;
String out_cmd = "";

int last_state_x = 90;
int command;
int data;

char str_data[30];
int iter = 0;

//ros data communication stuff

ros::NodeHandle  nh; //ros node handler
std_msgs::String str_msg; //ros message object

void head_data_in(const std_msgs::String& rec_msg)
{
  in_cmd = rec_msg.data;
}

ros::Publisher ard_pub_head("data_to_pc", &str_msg); //ros - arduino to pc
ros::Subscriber<std_msgs::String> ard_sub_head("data_to_arduino", &head_data_in ); //ros - pc to arduino
//ros data communication stuff

void setup()
{
  Serial.begin(57600); 

  pinMode(servo_pin_x,OUTPUT);
    
  nh.initNode();
  nh.advertise(ard_pub_head);
  nh.subscribe(ard_sub_head);

  move_servo(1, 80);
}

void loop()
{ 
  //deaing with data from the PC to Arduino
  if (in_cmd[0] == 'X')
  {
    command = in_cmd.substring(1).toInt(); 
    command = 180 - ((command/100.0)*180);
    move_servo(1, command);
  }
  
  //dealing with data from Arduino to PC
  data = analogRead(A0);
  //itoa(150, data, 10);
  out_cmd = out_cmd + data + ",";
  
  if(iter>1)
  {
    out_cmd.toCharArray(str_data,(out_cmd.length()+1));
    str_msg.data = str_data;
    ard_pub_head.publish( &str_msg );
    iter = 0;
  }
  out_cmd = "";
  iter++;

  Serial.println();
  nh.spinOnce(); 

  Serial.flush();
  
}
