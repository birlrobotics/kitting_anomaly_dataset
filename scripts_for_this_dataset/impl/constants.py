import os

dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
cache_folder = os.path.join(dir_of_this_script, '..', 'cache')
rosbag_folder_names_txt = os.path.join(cache_folder, "rosbag_folder_names.txt")
video_names_txt = os.path.join(cache_folder, "video_names.txt")
good_rosbag_folder_names_txt = os.path.join(cache_folder, "good_rosbag_folder_names.txt")
bad_rosbag_folder_names_txt = os.path.join(cache_folder, "bad_rosbag_folder_names.txt")
dataset_folder = os.path.join(dir_of_this_script, '..', '..', 'dataset')
