### Overview
The dataset captures sensory-motor and video data for anomalous events during the Kitting. The dataset consists of 538 rosbags. 85 of those rosbags are paired with RGB video that was captured by an external camera placed directly in front of the robot. The size of the 538 rosbags is of 37GB whilst the size of all videos is of 3.1GB. The dataset is found as Extension 2 in the paper as well as in \cite{2018IJRR-supplement}.

### Data Description
The main content of our data-set is the sensory-motor recordings of the robot manipulator's experience while performing the manipulation task. Original experiments were conducted in the Rethink Baxter robot and we used the following data modalities:
- the right endpoint state: contains end-effector pose, twist, and a wrench defined from the joint torques (not used).
- the stamped wrench: obtained from a Robotiq FT 180 force-torque sensor installed on the right wrist (see Fig. \ref{fig:experimental_setup}).
- the tactile data: obtained from a custom designed tactile sensor (see Sec. \ref{sec:Acknowledgements}).
When anomalies are triggered, we also record: (i) the time-stamp at which the anomaly is flagged as well as the anomaly classification label.

### Recording Methodology
All sensory-motor signals exist as ROS topics in our system and as such recorded as ROSBags offline. When an anomaly is identified, we signal this event by sending a timestamped ROS message to a pre-defined topic that is also recorded as a rosbag. Anomaly classification labels are recorded in a txt file in a line-by-line basis. 

Mapping from data modalities to ROS topics is as follows:
- Baxter right endpoint state:  /robot/limb/right/endpoint\_state
- Robotiq force sensor FT 180:  /robotiq_force_torque_wrench
- Robotiq tactile sensor:  
   /TactileSensor4/Accelerometer, 
   /TactileSensor4/Dynamic
   /TactileSensor4/EulerAngle, 
   /TactileSensor4/Gyroscope, 
   /TactileSensor4/Magnetometer,
   /TactileSensor4/StaticData


Data Organization
The dataset is composed of folders that use the format: ''experiment_at_[time]''. Each folder represents a test trial in the kitting experiment. Within a given folder, there will be a rosbag ''record.bag'' and a txt file ''anomaly_labels.txt''. Each of these contain the rosbag topics mentioned in Sec. 10.2 and the recorded labels for the given experiment.

### Anomaly Data Extraction
To extract anomaly data, one should first focus on the topic ''/anomaly_detection_signal'' whose messages are effectively timestamps indicating when anomalies were identified. It's worth noting that a burst of anomaly timestamps might have been published to this topic for one anomaly. Therefore timestamps that are adjacent in time should be ignored. We recommend ignoring a timestamp if its distance to its precursor is less than 1 second. After anomaly timestamps are extracted, labels in the accompanied ''anomaly_labels.txt'' can be paired accordingly. 

###  Corrupted data
We have tried to clear the dataset of any corrupted trials. However, if the number of anomaly timestamps does not equal to the number of labels, that experiment should be discarded. 