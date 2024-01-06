#! /usr/bin/env python
import math
import time
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.msg import Pos_Vel

def callback(msg):

	x_des = rospy.get_param("des_pos_x")
	y_des = rospy.get_param("des_pos_y")
	
	x = msg.x
	y = msg.y
	vel_x = msg.vel_x
	vel_z = msg.vel_z


	distance = math.sqrt(pow(x_des-x,2) + pow(y_des-y,2))
	
	avg_speed = math.sqrt(pow(vel_x,2)+pow(vel_z,2))
	
	print("Distance from the goal: ", distance)
	print("Average speed: ", avg_speed)

def main():

	rospy.init_node("nodeC")
	
	freq = rospy.get_param("freq")
	rate = rospy.Rate(freq)
	
	rospy.Subscirber("/info_pos_vel", Pos_Vel, callback)
	
	while not rospy.is_shutdown():
		
		rate.sleep()
	
	rospy.spin()

if __name__ == "__main__":
	main()


