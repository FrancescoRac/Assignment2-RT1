#include "ros/ros.h"
#include "turtlesim/Pose.h"
#include "geometry_msgs/Twist.h"
#include "turtlesim/Spawn.h"
//Add the required header
#include "turtlesim/Kill.h"
#include "msg/VelPos.msg"
#include "srv/Coordinates.srv"


ros::Publisher pub;


int main(int argc, char **argv)
{
	
	ros::init(argc, argv, " ");  
	ros::NodeHandle nh;
	
	
}
