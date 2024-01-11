# Assignment2-RT1

Second project developed for Research Track 1 for Robotics Engineering master degree at UniGe.

## Simulator

### ROS

ROS is an open-source meta-operating system, for robots. It provides services that you would expect from an operating system, including:

* Hardware abstraction;
* Low-level device control;
* Imlpementation of commonly-used functionality;
* Message-passing between processes;
* Package management.

### Gazebo
Gazebo is a 3D simulator for ROS.
The robot may be controlled using ROS topics. When moving the robot around, information coming from sensor may be visualized in Rviz.

### Rviz
Rviz is a tool for ROS Visualization. It's a 3D visualization tool for ROS. It allows the user to see the simulated robot model, log sensor information from the robot's sensors and replay the logged sensor information. By visualizing what the robot is seeing, thinking and doing, the user can debug a robot application from sensor inputs to planned actions.


## Description of the assignment
The aim of the project is to develop three nodes:
* `Node A`: implements an action client, allowing the user to set a target (x,y) or cancel it. Try to use the feedbeack/status of the action server to know when the target has been reached. The node also publishes the robot position and velocity as a custom message (x, y, vel_x, vel_z) by relying on the values published on topic/odom.

* `Node B`: implements a service node that, when called, returns the coordinates of the last target sent by the user.

* `Node C`: implements a service that subscribes to the robot's position and velocity (using the custom message) and implements a server to retrive the distance from the goal and the robot's average speed.

The following image show the nodes described above and the simulator:

![RT2](https://github.com/FrancescoRac/Assignment2-RT1/assets/93876265/91a4da99-aaa3-44b1-8633-901545081ad8)

## Motion of the robot

The robot can move in the environment which is an arena with obstacles (walls), the following scripts allow to the robot to reach the target point sent by the user, avoid obstacles and determine the robot actions based on the "change_state function".

`go_to_point_service`: service which allows the robot to move toward the desired position sent by the user and check if the robot can reach it.

`bug_as`: service that allow the user to determine the the robot's behavior by the state machine, which transitions between `go_to_point_service` and `wall_follow_service` states based on laser scan data and proximity to the goal.

`wall_follow_service`: service which allows to the robot to don't hit the obstacles in the arena and turn in order to follow the walls and avoid them.

## How to run the code
First of all you should have ROS installed, if you don't have please install ROS using the following link:

* Go on https://wiki.ros.org/ROS/Installation and follow the instruction.

Then you should follow the following steps:

* Clone this repository in your machine.
```
$ git clone https://github.com/FrancescoRac/Assignment2-RT1.git
```

* Run the `roscore` command to launch the master sevrice.

* Digit `catkin_make` in your root directory, this command allow you to build packages, compiling and generate executable files from source code.

* If you don't have installed `xterm` yet, please install it using the following command `sudo apt-get install xterm`. Xterm is the standard terminal emulator for the X Window System. It allows users to run programs which require a command line interface.

* To run the code each file in the folder `scripts` must be executble, if there is a file which is not, then use the command `chmod +x "Filename"` to make it executable.

* Use the command `roslaunch assignment_2_2023 assignment1.launch`, which is a command to read the launch file, such that it will run each file write in the launch file.

## Pseudocode Node A

1. Initialize ROS node `nodeA`
2. Create a global variable `publisher` and set it to None
3. Define a callback function `callback` that takes a message `msg` as input:
   * Extract position, linear velocity, and angular velocity from `msg`
   * Create a `Pos_Vel` message and populate it with extracted values
   * Publish the `Pos_Vel` message using the `publisher`

4. Define a function `client_request`:
    * Initialize a SimpleActionClient for the `PlanningAction` server (`/reaching_goal`)
    * Wait for the action server to become available
    * Enter a loop that continues until rospy is shutdown:
        * Get the current goal position parameters from ROS parameters
        * Create a `PlanningGoal` message with the target position
        * Prompt the user to enter new goal coordinates:
            * Validate the input, ensuring it's within the valid range
        * Set the new goal coordinates as ROS parameters
        * Send the new goal to the action server
        * Enter a loop that continues until the user decides to cancel or set a new goal:
            * Prompt the user for input ('c' to cancel, 'y' to set a new goal)
            * If 'c' is entered, cancel the current goal and log the cancellation
            * If 'y' is entered, set a new goal and break out of the loop
            * If an invalid input is provided, log a warning and continue the loop
        * Log the last received goal coordinates

5. Define the `main` function:
    * Initialize the ROS node `nodeA`
    * Create a global `publisher` variable and set it to a publisher for the `/pos_vel` topic
    * Subscribe to the `/odom` topic with the `callback` function
    * Call the `client_request` function

6. Check if the script is being run as the main module:
    * If true, call the `main` function


## Code Developed
### Node A
This node allows to the user to set a target or cancel it.
The first target is the one which is set in the launch file "assignment1.launch", then the node ask to the user to set a new target and once it is set, the user can choose if enter again a new target or cancel the previous one.
Once that the target is set it is possible to see the position and the velocity of the robot as a custom message using the command "rostopic echo pos_vel".

It is composed by three functions:

* `main()`: which initialize the node, create the publisher and subscribe to the `/odom` topic;

* `client_request()`: create a simple action client and allows to the user to set the target or cancel it till ROS is shutdown. This function allow to the client to send the goal or cancel it using the function `client.send_goal()` and `client.cancel_goal`;

* `callback(msg)`: which extract the position and velocity from the `/odom` topic, create a new custom message with the value taken from the topic and publish them with the function `publisher.publish("CreatedMessage")`.

### Node B: 
This node allows to the user to see the last target coordinates sent by the user using `Coordinates` service. 
The script subscribes to the `/reaching_goal/goal` topic and listens for messages of type `assignment_2_2023.msg.PlanningActionGoal`

It is composed by three functions:

* `main()`: which initialize the node, initialize the service and subscribe to the `/reaching_goal/goal`;

* `take()`: takes the value of the last coordinates and assigns them to `coord`;

* `give_back_last_goal(msg)`: which extracts the last coordinate value on the x and y axes from the message and assigns them to `last_coord_x` and `last_coord_y`, respectively.

The information are visible in an xterm window but it is also possible to visualize the last coordinates that the user set using the following command in a new terminal:
```
rosservice call /srv
```

### Node C: 
This node allow to the user to visualize the average speed of the robot and the distance fo the robot from the last target sent by the user.

It is composed by three functions:

* `main()`: initializes the service, subscribes to the /pos_vel topic, and calls the take_values function to return the distance from the goal and the average speed;

* `take_values()`: returns the distance from the goal and the average speed using the `Dist_AvgSpeedResponse` service;

* `callback(msg)`: which extracts the current position of the robot and the desired position of the robot from the message and calculates the distance between them.

## Further imporovement

* Implement function to understand the dimension of the arena.

* Node C -> when the message is published there is a little change of the value even if the robot is not moving and turning, a threshold could be set in order to don't take into account small changes.



















