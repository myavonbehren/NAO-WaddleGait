# NAO Robot Waddle Gait

## Introduction
During the Spring Quarter of my second year, I worked with [Aldebaran Robotics’ NAO humanoid robot](https://www.aldebaran.com/en/nao) to explore its walking gait. Using [Aldebaran's Python Software Development Kit](http://doc.aldebaran.com/2-5/dev/python/install_guide.html) (SDK), NAOqi, I was able to create Python modules to control NAO’s walking gait. Before installing the Python SDK, I downloaded Python 2.7 - 32 bits, the only compatible version allowing NAOqi to run correctly. 

NAOqi provides a comprehensive API allowing users to interact with NAO in various ways, including audio, vision, communication, and motion. I primarily focused on the motion API known as NAOqi Motion which deals with the robot’s movement, including its walk. Within the [ALMotion API](http://doc.aldebaran.com/2-5/naoqi/motion/almotion.html), users have control over essential aspects of the robot, including joint stiffness, joint position, and robot effector in the Cartesian space. 

Under the ALMotion API, I worked with the [Locomotion Control API](http://doc.aldebaran.com/2-5/naoqi/motion/control-walk.html#control-walk), a set of methods that allow users to move the robot to various places. According to Aldebaran’s documentation for the locomotion control API, there are three high-level ways to control the locomotion, ALMotionProxy::moveTo which allows users to move the robot to a target pose on the ground, ALMotionProxy::move which enables users to set the robot’s direction and intensity in SI units, and the ALMotionProxy::moveToward which enables interactive control over the robot’s speed by allowing you to set its velocity. Other ways to control locomotion focus more on managing the robot’s footsteps. 

To explore and customize the walking gait of NAO, I used the [ALMotionProxy::moveToward](http://doc.aldebaran.com/2-5/naoqi/motion/control-walk-api.html#ALMotionProxy::moveToward__floatCR.floatCR.floatCR) method. The moveToward method takes in four parameters:
* The ‘x’ parameter determines the velocity along the x-axis, enabling the robot to move forward and backward at the given speed. A positive value with a maximum velocity of +1 allows the robot to move forward, while a negative value with a minimum velocity of -1 allows the robot to move backward.
* The ‘y’ parameter determines the velocity along the y-axis, which allows the robot to move right and left. Similar to the ‘‘x’ parameter, a positive value with a maximum velocity of +1 allows the robot to move left. In contrast, a negative value with a minimum velocity of -1 enables the robot to move right.
* The ‘theta’ parameter determines the velocity, allowing the robot to rotate clockwise or counterclockwise. As with the ‘x’ and ‘y’ parameters, the ‘y’ parameter also has a maximum positive value of +1, which moves the robot counterclockwise, and a minimum negative value of -1, which moves the robot clockwise.
* The ‘[moveConfig](http://doc.aldebaran.com/2-5/naoqi/motion/control-walk.html#move-config)’ parameter takes in an ALValue (list in Python) and allows users to customize the gait parameters for NAO’s walk. The ‘moveConfig’ is defined by a set of parameters users can adjust; users can find the parameters [here](http://doc.aldebaran.com/2-5/naoqi/motion/control-walk.html#control-walk-gait-parameters-table).

After fully understanding what the moveToward method does and all the parameters needed, I searched for various examples in which users used the method. Luckily, Aldebaran’s documentation provided some, including almotion_moveCustomization.py, which customizes NAO’s walking gait to look like Keyser Sose in The Usual Suspects. NAO walks with a limp and then walks correctly. 
Using [almotion_moveCustomization.py](http://doc.aldebaran.com/2-5/_downloads/almotion_moveToward.py) as a reference and a foundation, I created a customized walking gait for NAO. This gait emulates a waddle, often seen in penguins and ducks. This waddling gait is slower than the average walking gait and is characterized by side-to-side movement. Further, each foot has a lower lift off the ground than a typical walking gait.

## Breakdown
The most notable change I made within the [almotion_moveCustomization.py](http://doc.aldebaran.com/2-5/_downloads/almotion_moveToward.py) was adjusting the moveToward function. Below is the modified moveToward function that makes NAO have a waddling gait. 

```python
motion_service.moveToward(X, Y, Theta,[["Frequency", Frequency],
# LEFT FOOT
["LeftStepHeight", 0.005],
["LeftTorsoWx", -5.5*almath.TO_RAD],
["LeftTorsoWy", 5.0*almath.TO_RAD],
["LeftMaxStepX", 0.02], 
["LeftMaxStepY", 0.15],
["LeftMaxStepFrequency", 0.5],
# RIGHT FOOT
["RightStepHeight", 0.005],
["RightMaxStepX", 0.02],
["RightMaxStepY", 0.15],
["RightMaxStepFrequency", 0.5],
["RightTorsoWx", 5.5*almath.TO_RAD],
["RightTorsoWy", 5.0*almath.TO_RAD]
])
```
The StepHeight parameter adjusts the foot elevation along the Z-axis. The step height is 0.005 meters, the minimum value for the StepHeight parameter. It is also 0.015 meters less than the default value of 0.02 meters.

```python
["LeftStepHeight", 0.01]
["RightStepHeight", 0.01]
```

The TorsoWx and TorsoWy parameter adjusts the rotation angle of the torso along the x- and y-axis for each foot. TorsoWx allows users to move the torso right and left while walking, while TorsoWy enables users to move the torso forward and backward. To replicate a waddling gait, where the robot moves side-to-side, adjusting the left and right TorsoWx is necessary.  LeftTorsoWx is set to -5.5 degrees which is -5.5 degrees from the default value of 0.0 degrees. RightTorsoWy is set to 5.5 degrees which is 5.5 degrees from the default value of 0.0 degrees. By having LeftTorsoWx and RightTorsoWy in opposite directions, the robot moves side to side. This angular difference creates a tilting motion in the torso, resulting in the characteristic side-to-side movement observed in a waddling gait. The TorsoXy is the same for both as it adjusts the forward direction of the torso; this is set to 5.0 degrees which deviates 5.0 degrees from the default value of 0.0 degrees. This value is set so high to allow stability for the robot’s torso since it constantly moves from side to side. By adjusting the forward direction of the torso, the robot maintains a more balanced posture and improves its overall stability while executing the waddling motion.

```python
["LeftTorsoWx", -5.5*almath.TO_RAD]
["LeftTorsoWy", 5.0*almath.TO_RAD]
["RightTorsoWx", 5.5*almath.TO_RAD]
["RightTorsoWy", 5.0*almath.TO_RAD]
``` 

MaxStepX and MaxStepY determine the maximum step lengths or distance in meters for the robot to move forward/backward in the x-axis and y-axis direction. The MaxStepX for the left and right foot is set to 0.02 meters, which is 0.02 meters less than the default value of 0.40 meters. This adjustment ensured NAO took shorter steps while walking forward. The MaxStepY is set to the default value of 0.14 because the waddling gait does not include backward walking. 

```python
["LeftMaxStepX", 0.02]
["LeftMaxStepY", 0.15]
["RightMaxStepX", 0.02]
["RightMaxStepY", 0.15]
```

The MaxStepFrequency adjusts the pace or speed of the robot’s walking gait. This unitless value determines how quickly each foot can take consecutive walking steps. For the left and right feet, the value was set to 0.5, 0.5 more than the default, to create a slower walk. 

```python
["LeftMaxStepFrequency", 0.5],
["RightMaxStepFrequency", 0.5]
```

## Conclusion
After implementing the waddling gait for NAO, I gained several insights and learned valuable lessons about embedded systems and software development. I now understand walking gaits and the many characteristics of implementing a successful gait. I also have a deeper understanding and appreciation for the nuances and variations in robotic locomotion. 

Further, implementing the waddling gait was a long and iterative process of trial and error. I learned the importance of testing, analyzing results, and making incremental adjustments to refine the gait. I learned the importance of customization and adaptation in robot programming. I realized how these adjustments could significantly alter the robot's gait and overall behavior by modifying parameters such as step length, torso angles, and maximum step frequency. Lastly, I gained hands-on experience utilizing motion control APIs and learned to manipulate various parameters to achieve desired movements. 
