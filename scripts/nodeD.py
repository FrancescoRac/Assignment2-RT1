#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from assignment_2_2023.msg import Obs


publisher = None


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
	

# Main function
def main():

    # Create an instance of the service class
    rospy.init_node('nodeD')
    rospy.loginfo("Info service node initialized")
    
    global pub

    pub = rospy.Publisher("/obs", Obs, queue_size=1)
    
    rospy.Subscriber("/scan", LaserScan, min_distance)
    
            
    rospy.spin()
    
if __name__ == "__main__":
    main()
