#! /usr/bin/env python
import sys
import select
import rospy
import actionlib
import actionlib.msg
import math
import time
import assignment_2_2023.msg

from assignment_2_2023.msg import pos_vel
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
from std_srvs.srv import *


def callback(msg):

	global publisher

	pos = msg.pose.pose.position
	
	vel = msg.twist.twist.linear
	
	msg_new = pos_vel()
	
	msg_new.x = position.x
	
	msg_new.y = position.y
	
	msg_new.vel_x = velocity.x
	
	msg_new.vel_z = velocity.z
	
	publisher.publish(msg_new)	
		
	
	
def client_request():

	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)
	client.wait_for_server()
	
	while not rospy.is_shutdown():
		
		try:
			x_des = float(input("Set x coordinate: "))
			y_des = float(input("Set y coordinate: "))
		except:
			print("Invalid coordinates")
			continue
			
		target = assignment_2_2023.msg.PlanningGoal()
			
		target.target_pose.pose.position.x = x_des
		target.target_pose.pose.position.y = y_des
			
		client.send_goal(target, None, None)
		
		target_reached = False
		
		print("\nEnter 'c' to cancel the goal: ", end="")
		
		while not target_reached:
		
			tof = select.select([sys.stdin], [], [], 1)[0]
			
			if tof:
			
				value = sys.stdin.readline().rstrip()
				
				if value == 'c':
				
					print("Goal cancelled")
					client.cancel_goal()
					target_reached = True
	
	
	
def main():

	rospy.init_node('nodeA')
	
	global publisher
	publisher = rospy.Publisher("/PosVel", PosVel, queue_size = 1)
	
	rospy.Subscriber('/odom', Odometry, callback) 
	
	global client
	
	client_request()
	
		
if __name__ == ' __main__':

	main()

		
		 
