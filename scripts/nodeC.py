#!/usr/bin/env python

import rospy
import math
from assignment_2_2023.msg import Pos_Vel
from assignment_2_2023.srv import Dist_AvgSpeed, Dist_AvgSpeedResponse

'''
This node allow to the user to visualize the average speed of the robot 
and the distance fo the robot from the last target sent by the user.
'''
       
distance = 0.0
avg_speed = 0.0
window = []

def callback(msg):
    
    global distance, avg_speed

    # get the value related to the desired position of the robot (target position)
    des_x = rospy.get_param('/des_pos_x')
    des_y = rospy.get_param('/des_pos_y')

    window_size = rospy.get_param('/window_size')
    
    x = msg.x
    y = msg.y
    
    # Calculate the distance from the target using the desired position and the current position
    distance = math.sqrt(pow(des_x-x,2) + pow(des_y-y,2))

    if len(window) > window_size:
    	window.pop(0) # delete the first value in the array when the size exceed the window_size
    	
    window.append(math.sqrt(pow(msg.vel_x,2) + pow(msg.vel_z,2))) # add to the array the value of the speed
    
    avg_speed = sum(window) / window_size


def take_values(_):
    # return the distance from the goal and the average speed using Dist_AvgSpeedResponse service
    return Dist_AvgSpeedResponse(distance, avg_speed)		      

# Main function
if __name__ == "__main__":

    # Create an instance of the service class
    rospy.init_node('info_service')
    rospy.loginfo("Info service node initialized")

    # Provide a service named 'info_service', using the custom service type Dist_AvgSpeed
    rospy.Service("info_service", Dist_AvgSpeed, take_values)
    
    # Subscribe to the '/pos_vel' topic, using the custom message type Pos_Vel
    rospy.Subscriber("/pos_vel", Pos_Vel, callback)
    
    service = rospy.ServiceProxy('info_service', Dist_AvgSpeed)

    while not rospy.is_shutdown():
            # Call the service
            response = service()
 
            rospy.loginfo(f"Service response:\n {response}")
            
    rospy.spin()
