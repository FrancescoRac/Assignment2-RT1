#! /usr/bin/env python
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.msg
from nav_msgs.msg import Odometry
#from std_srvs.srv import SetBool, Empty
from std_srvs.srv import *
from assignment_2_2023.msg import Pos_Vel, Pos_Goal
from assignment_2_2023.srv import CancelGoal, CancelGoalResponse
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2023.msg import PlanningAction, PlanningGoal, PlanningResult
from sensor_msgs.msg import LaserScan
from assignment_2_2023.msg import Obs
from assignment_2_2023.srv import Coordinates, CoordinatesResponse

'''
This node allows the user to set a target or cancel it. 
It also publish the robot's position and velocity as custom message.
To see the custom message, while the node is running enter "rostopic echo pos_vel" on the prompt.
'''


# Global variables
publisher= None

# Publisher function
def callback(msg):
	global publisher
	# Extract position, linear velocity and angular velocity from the message
	pos = msg.pose.pose.position
	vel = msg.twist.twist.linear
	ang = msg.twist.twist.angular
	
	# Create a new Pos_Vel message
	posvel = Pos_Vel()
	
	# Give the value related to position and velocity to the message
	'''
	Uncomment the following lines if you want the position of the robot in feet
	'''
	#posvel.x = pos.x*3.28
	#posvel.y = pos.y*3.28
	
	'''
	Position in meters
	Velocity in m/s
	'''
	posvel.x = pos.x
	posvel.y = pos.y
	#posvel.z = pos.z	Uncomment this row if you want also the z coordinate and add in the Pos_Vel.msg what is written in the brackets (float64 z)
	posvel.vel_x = vel.x
	posvel.vel_z = ang.z
	
	# Publish the message
	publisher.publish(posvel)

# Client function
def client_request():
	global x
	global y
	global client
	# Create a SimpleActionClient
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)
	client.wait_for_server()

	# Loop until ROS is shutdown
	while not rospy.is_shutdown():
		
		# Get the current goal position
		x_param = rospy.get_param('/des_pos_x')
		y_param = rospy.get_param('/des_pos_y')
		
		# Create a new PlanningGoal
		target = assignment_2_2023.msg.PlanningGoal()
		target.target_pose.pose.position.x = x_param
		target.target_pose.pose.position.y = y_param
		rospy.loginfo("Current goal: target_x = %f, target_y = %f", x_param, y_param)
		
		# If the user wants to set a new goal	
		print("Set the coordinates of the goal")

		
		try:
			x = float(input("Enter the x-coordinate for the new goal: "))
			y = float(input("Enter the y-coordinate for the new goal: "))
				
			if (x > 9.0 or y > 9.0 or x < -9.0 or y < -9.0):
				print("Please enter a valid input \nInput values must be between -8.0 and 8.0")
				continue
		except ValueError:
			
			rospy.logwarn("Invalid input. Please enter a valid number.")
			continue
			
		# Set the new goal position
		rospy.set_param('/des_pos_x', x)
		rospy.set_param('/des_pos_y', y)
			
		target.target_pose.pose.position.x = x
			
		target.target_pose.pose.position.y = y
			
		# Send the new goal
		client.send_goal(target)
		
		rospy.wait_for_service("/srv")
		last_goal = rospy.ServiceProxy("/srv", Coordinates)
		goal = last_goal()
		print(goal)
		
		goal_canc = False
		
		# while goal_canc is False ask to the user if cancel the goal or set a new goal
		while goal_canc is False:
			
			canc = input("Insert 'c' if you want to cancel the goal otherwise type 'y' to insert a new goal or you can type 'r' to reset the simulation ( do not press r service momentarily out of service) : ")
			
			
			# If the user wants to cancel the current goal
			if canc == 'c':
			
				client.cancel_goal()
				rospy.loginfo("Current goal has been cancelled")
				goal_canc = True
				
			# If the user wants to set a new goal	
			elif canc == 'y':
				print("Set a new goal")
				goal_canc = True
				continue
			
			elif canc == 'r':
				client.cancel_goal()
				rospy.wait_for_service("/gazebo/reset_world")
				reset_world = rospy.ServiceProxy("/gazebo/reset_world", Empty)
				reset_world()
				goal_canc = True
			
			else:
				rospy.logwarn("Invalid command. Please enter 'y' to insert a new goal or 'c' to cancel the current goal.")
				continue
			
		rospy.loginfo("Last received goal: target_x = %f, target_y = %f", target.target_pose.pose.position.x, target.target_pose.pose.position.y)
		
		window = False
		
		while window is False:
		
			press = input("If you want change the window size press 'y', otherwise press 'n': ")
			
			if press == "y":
				window_size = float(input("Enter the size of the window: "))
				rospy.set_param('/window_size', window_size)
				rospy.loginfo(window_size)
				window = True
				
			
			if press == "n":
				
				window = True
		

def cancCallback(_):

	cancel = CancelGoalResponse()
	
	client.cancel_goal()
	
	return cancel
	
	
def min_distance(msg):

	obs = Obs()
	
	obs.obsDistance = min([
		min(min(msg.ranges[0:143]), 10), 
		min(min(msg.ranges[144:287]), 10), 
		min(min(msg.ranges[288:431]), 10), 
		min(min(msg.ranges[432:575]), 10), 
		min(min(msg.ranges[576:713]), 10),
		])
	      
	pub.publish(obs)


def callGoal(msg):

	global pub_goal
	
	pos_goal = Pos_Goal()
	
	pos_goal.x = msg.goal.target_pose.pose.position.x
	pos_goal.y = msg.goal.target_pose.pose.position.y
	pos_goal.z = msg.goal.target_pose.pose.position.z

	pub_goal.publish(pos_goal)
	

# Main function
def main():

	# Initialize the node
	rospy.init_node('nodeA')
	
	global publisher, pub, pub_goal
	
	# Create a publisher
	publisher = rospy.Publisher("/pos_vel", Pos_Vel, queue_size=1)
	
	# Subscribe to the /odom topic
	rospy.Subscriber("/odom", Odometry, callback)
	
	rospy.Service("/cancel_goal", CancelGoal, cancCallback) 
	
	pub = rospy.Publisher("/obs", Obs, queue_size=1)
    
	rospy.Subscriber("/scan", LaserScan, min_distance)
	
	pub_goal = rospy.Publisher("/pos_goal", Pos_Goal, queue_size = 1)
	
	rospy.Subscriber("/reaching_goal/goal", assignment_2_2023.msg.PlanningActionGoal, callGoal)
	
	# Run the client function
	client_request()

# Entry point
if __name__ == '__main__':
	main()
