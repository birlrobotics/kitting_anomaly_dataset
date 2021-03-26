import constants as c
import logging
import os
import shutil
import multiprocessing

def copy_folder(source_folder):
    shutil.copytree(source_folder, os.path.join(c.dataset_folder, os.path.basename(source_folder))) 

def run():
    logger = logging.getLogger("build_up_dataset_of_good_bags")
    logger.info("Building dataset")

    shutil.rmtree(c.dataset_folder, ignore_errors=True)

    pool = multiprocessing.Pool() 
    async_results = []
    with open(c.good_rosbag_folder_names_txt, 'r') as good_txt:
        for line in good_txt:
            async_result = pool.apply_async(copy_folder, args=(line.strip(),))
            async_results.append((line.strip(), async_result))

    for line, async_result in async_results:
        async_result.wait()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    run()
