# Assignment2-RT1

Second project developed for Research Track 1.
Robotics Engineering master degree.

## Simulator

### Gazebo
Gazebo is a 3D simulator for ROS.
The robot may be controlled using ROS topics. When moving the robot around, information coming from sensor may be visualized in Rviz.

### Rviz
Rviz is a tool for ROS Visualization. It's a 3D visualization tool for ROS. It allows the user to see the simulated robot model, log sensor information from the robot's sensors and replay the logged sensor information. By visualizing what the robot is seeing, thinking and doing, the user can debug a robot application from sensor inputs to planned actions.

## Motion of the robot

The robot can move in the environment which is an arena with obstacles (walls), the following functions allow to the robot to reach the target point sent by the user, avoid obstacles and determine the robot actions based on the "change_state fucntion".

`go_to_point_service`:

`bug_as`:

`wall_follow_service`:


## Description of the assignment
The aim of the project is to develop three nodes:
* `Node A`: implements an action client, allowing the user to set a target (x,y) or cancel it. The node also publishes the robot position and velocity as a custom message (x, y, vel_x, vel_z) by relying on the values published on topic/odom.

* `Node B`: implements a service node that, when called, returns the coordinates of the last target sent by the user.

* `Node C`: implements a service that subscribes to the robot's position and velocity (using the custom message) and implements a server to retrive the distance from the goal and the robot's average speed.

## How to run the code



## Flowchart


## Code Developed

### Node A

### Node B

### Node C


## Further imporovement




















