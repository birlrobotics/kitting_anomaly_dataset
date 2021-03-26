import constants as c
import logging
import rosbag
import os
import multiprocessing

topics_to_check = set([
    '/TactileSensor4/Accelerometer',
    '/TactileSensor4/Dynamic',
    '/TactileSensor4/EulerAngle',
    '/TactileSensor4/Gyroscope',
    '/TactileSensor4/Magnetometer',
    '/TactileSensor4/StaticData',
    '/anomaly_detection_signal',
    '/robot/limb/right/endpoint_state',
    '/robotiq_force_torque_wrench'])

def check_bag(folder_path):
    bag_path = os.path.join(folder_path, 'record.bag')
    if not os.path.isfile(bag_path):
        return (False, "not os.path.isfile(bag_path)")

    with open(bag_path, 'rb') as bag_f:
        bag = rosbag.Bag(bag_f)
        type_info, topic_info = bag.get_type_and_topic_info()
        topics_contained = set(topic_info.keys())

        if not topics_to_check.issubset(topics_contained):
            return (False, "not topics_to_check.issubset(topics_contained)")
        
        signals = []
        for topic_name, msg, gen_time in bag.read_messages(topics=["/anomaly_detection_signal"]):
            if len(signals) == 0:
                signals.append(msg)
            else:
                time_diff = (msg.stamp-prev_msg.stamp).to_sec()
                if time_diff > 1:
                    signals.append(msg)
                elif time_diff < 0:
                    raise Exception("Weird error: messages read from rosbag are not in time-increasing order")
            prev_msg = msg

    label_path = os.path.join(folder_path, 'anomaly_labels.txt')
    if len(signals) == 0:
        if os.path.isfile(label_path):
            return (False, "len(signals) == 0 but os.path.isfile(label_path)")
    else:
        if not os.path.isfile(label_path):
            return (False, "not len(signals) == 0 but not os.path.isfile(label_path)")

        with open(label_path, 'r') as label_f:
            label_amount = len([i for i in label_f.readlines() if i.strip() != ""])
            if label_amount != len(signals):
                return (False, "label_amount %s != len(signals) %s"%(label_amount, len(signals)))
    return (True, None)

def run():
    logger = logging.getLogger("filter_bad_bags")
    logger.info("Filtering bad bags")

    pool = multiprocessing.Pool() 
    async_results = []
    with open(c.rosbag_folder_names_txt, 'r') as txt:
        for line in txt:
            async_result = pool.apply_async(check_bag, args=(line.strip(),))
            async_results.append((line.strip(), async_result))

    with open(c.good_rosbag_folder_names_txt, 'w') as good_txt,\
        open(c.bad_rosbag_folder_names_txt, 'w') as bad_txt:
        for line, async_result in async_results:
            is_good, debug_info = async_result.get()
            if is_good  == True:
                good_txt.write(line)
                good_txt.write('\n')
            else:
                bad_txt.write(line)
                bad_txt.write(" ")
                bad_txt.write(debug_info)
                bad_txt.write('\n')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run()
