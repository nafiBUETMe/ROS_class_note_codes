void move_servo(int num, int state)
{
  if((num == 1) && (last_state_x != state))
  {
    if(state > last_state_x)
    {
      while(state != last_state_x)
      {
        int onTime = map(last_state_x,0,180,250,2500);
        int offTime = 20000 - onTime;
        digitalWrite(servo_pin_x,HIGH);
        delayMicroseconds(onTime);
        digitalWrite(servo_pin_x,LOW);
        delayMicroseconds(offTime);
        delay(50);
        last_state_x = last_state_x+1;
      }
    }
    else if(state < last_state_x)
    {
      while(state != last_state_x)
      {
        int onTime = map(last_state_x,0,180,250,2500);
        int offTime = 20000 - onTime;
        digitalWrite(servo_pin_x,HIGH);
        delayMicroseconds(onTime);
        digitalWrite(servo_pin_x,LOW);
        delayMicroseconds(offTime);
        delay(50);
        last_state_x = last_state_x-1;
      }
    }
  }
}
