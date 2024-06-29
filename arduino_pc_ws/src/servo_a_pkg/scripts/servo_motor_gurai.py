#! /usr/bin/python3

import rospy
from std_msgs.msg import String


if __name__=='__main__':
    rospy.init_node('pc_server',anonymous=True)

    pub = rospy.Publisher('pc_to_arduino',String,queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        
        str = input("Enter command: ")  #  here we will give anti 20 or clock 20
        pub.publish(str)

        rate.sleep()

