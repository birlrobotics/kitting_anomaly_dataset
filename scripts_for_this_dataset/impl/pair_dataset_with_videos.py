import constants as c
import logging
import os
import shutil
import multiprocessing

def copy_video(video):
    shutil.copy(video, os.path.join(c.dataset_folder, os.path.basename(video)[:-4])) 

def run():
    logger = logging.getLogger("pair_dataset_with_videos")
    logger.info("Paring dataset with videos")

    pool = multiprocessing.Pool() 
    async_results = []
    with open(c.good_rosbag_folder_names_txt, 'r') as good_txt, \
        open(c.video_names_txt, 'r') as video_txt:
        videos = dict([(os.path.basename(i.strip())[:-4], i.strip()) for i in video_txt if i.strip() != ""])
        for line in good_txt:
            exp_name = os.path.basename(line.strip())
            if exp_name in videos:
                async_result = pool.apply_async(copy_video, args=(videos[exp_name],))
                async_results.append((line, async_result))

    for line, async_result in async_results:
        async_result.wait()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run()
