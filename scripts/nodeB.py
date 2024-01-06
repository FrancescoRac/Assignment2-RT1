#! /usr/bin/env python
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
from nav_msgs.msg import Odometry
from std_srvs.srv import SetBool
from assignment_2_2023.msg import Coordinates
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2023.msg import PlanningAction, PlanningGoal, PlanningResult


def main():

	# Initialize the node
	rospy.init_node('nodeB')
	
	global publisher
	
	# Create a publisher
	publisher = rospy.Publisher("/pos_vel", pos_vel, queue_size=1)
	
	# Subscribe to the /odom topic
	rospy.Subscriber("/odom", Odometry, callback)
	
	# Run the client function
	client_request()

# Entry point
if __name__ == '__main__':
	main()
