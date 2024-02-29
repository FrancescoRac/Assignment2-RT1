#! /usr/bin/env python


"""
.. module nodeB

   :platform unix
   :synopsys:Brief description of the file
	
.. :moduleauthor:: Francesco Rachiglia ceccorac@gmail.com

ROS node that allows to the user to see the last coordinates sent by the user using the "Coordinates" service. 

Subscrbes to:

	/reaching_goal/goal
	
Services:

	/Coordinates
	
"""

import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.srv import Coordinates, CoordinatesResponse

'''
This node allows to the user to see the last coordinates sent by the user using the "Coordinates" service. 
'''

last_coord_x = 0.0
last_coord_y = 0.0

def give_back_last_goal(msg):

	"""
	give_back_last_goal Function:
		get the last desired position inserted by the user.
	
	Args(/reaching_goal/goal): that contain the coordinates of the last goal.
	
	"""

	global last_coord_x, last_coord_y

	# Take the last coordinate value
	last_coord_x = msg.goal.target_pose.pose.position.x
	last_coord_y = msg.goal.target_pose.pose.position.y
	
	print("Last coordinates: ")
	print("x =  ", last_coord_x)
	print("y =  ", last_coord_y)
	print("\n")
	
	
def take(_):

	"""
	take Function:
		take the response of the service Coordinate which gives the last coordinates of the desired position.
		
	Parameters:
		coord: parameter that has the x and y coordinate of the desired position.
		
	Returns:
		the coordinates (x and y) of the desired position.
		
	"""

	global last_coord_x, last_coord_y
	
	# Take the value of the last coordinates and assign them to coord
	coord = CoordinatesResponse()
	
	# cx is the last coordinate value on x axis and cy is the last coordinate value on y axis 
	coord.cx = last_coord_x
	coord.cy = last_coord_y
	
	return coord
	

def main():

	# Initialize the node
	rospy.init_node('nodeB')
	
	# Initialize the service 
	rospy.Service("srv", Coordinates, take)
	
	# Subscribe to the /reaching_goal/goal topic
	rospy.Subscriber("/reaching_goal/goal", assignment_2_2023.msg.PlanningActionGoal, give_back_last_goal)
	
	rospy.spin()

if __name__ == '__main__':
	main()
