import logging
import impl

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    impl.collect_info_of_bag_and_video_sets.run()
    impl.filter_bad_bags.run()
    impl.build_up_dataset_of_good_bags.run()
    impl.pair_dataset_with_videos.run()
