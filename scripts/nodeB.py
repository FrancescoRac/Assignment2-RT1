#! /usr/bin/env python
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.srv import Coordinates, CoordinatesResponse

last_coord_x = 0.0
last_coord_y = 0.0

def give_back_last_goal(msg):

	global last_coord_x, last_coord_y

	last_coord_x = msg.goal.target_pose.pose.position.x
	last_coord_y = msg.goal.target_pose.pose.position.y
	
	print("\n\n")
	print("Last coordinate x =  ", last_coord_x)
	print("Last coordinate y =  ", last_coord_y)
	
	
def take():

	global last_coord_x, last_coord_y
	coord = CoordinatesResponse()
	coord.cx = last_coord_x
	coord.cy = last_coord_y
	
	return coord
		

def main():

	# Initialize the node
	rospy.init_node('nodeB')
	
	rospy.Service("srv", Coordinates, take)
	
	rospy.Subscriber("/reaching_goal/goal", assignment_2_2023.msg.PlanningActionGoal, give_back_last_goal)
	
	rospy.spin()

if __name__ == '__main__':
	main()
