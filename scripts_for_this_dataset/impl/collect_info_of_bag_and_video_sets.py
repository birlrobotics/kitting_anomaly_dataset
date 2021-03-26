import subprocess, shlex, os
import logging
import constants as c

def run(rosbag_base_dir=None, video_base_dir=None):
    logger = logging.getLogger("collect_info_of_bag_and_video_sets")
    logger.info("Collecting bags and videos")

    if rosbag_base_dir is None:
        print "Enter base directory from which to search rosbags:"
        rosbag_base_dir = raw_input()

    if video_base_dir is None:
        print "Enter base directory from which to search videos:"
        video_base_dir = raw_input()

    if not os.path.isdir(c.cache_folder):
        os.makedirs(c.cache_folder)

    open(c.rosbag_folder_names_txt, 'w').close()
    cmd = "find %s -path \"*experiment_at_*/record.bag\" -exec sh -c \'echo \"$(readlink -f $(dirname $0))\" >> %s\' {} \;"%(rosbag_base_dir, c.rosbag_folder_names_txt)
    logger.debug("Running command \"%s\""%cmd) 
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed to run command")

    open(c.video_names_txt, 'w').close()
    cmd = "find %s -name \"experiment_at_*.mp4\" -exec sh -c \'echo \"$(readlink -f $0)\" >> %s\' {} \;"%(video_base_dir, c.video_names_txt)
    logger.debug("Running command \"%s\""%cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed to run command")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run("data_for_test", "data_for_test")
