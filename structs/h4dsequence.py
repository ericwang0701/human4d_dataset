import os
import cv2
from structs import H4DFrame

from importers import *

class H4DSequence:
    def __init__(self, sequence_path, camera_ids):
        self.camera_ids = camera_ids
        self.cameras = {}
        self.init_groupframe_id = -1
        self.init_timestamp = {}
        init_timestamp_set = False
        for cam in camera_ids:
            self.cameras[cam] = []
        
        color_images = os.listdir(os.path.join(sequence_path, "color"))
        depth_images = os.listdir(os.path.join(sequence_path, "depth"))
        timestamps = os.listdir(os.path.join(sequence_path, "timestamp"))

        for i in range (len(color_images)):
            groupframe_id, cam, _, frame_id = color_images[i].split('_')
            frame_id = frame_id.split('.')[0]

            color_img = cv2.imread(os.path.join(sequence_path, "color", color_images[i]))
            depth_img = readpgm(os.path.join(sequence_path, "depth", depth_images[i])) / 10

            if (init_timestamp_set and int(groupframe_id) > self.init_groupframe_id):
                timestamp = float(open(os.path.join(sequence_path, "timestamp", timestamps[i])).readline()) - self.init_timestamp[cam]        
            else:
                timestamp = float(open(os.path.join(sequence_path, "timestamp", timestamps[i])).readline())
                self.init_timestamp[cam] = timestamp
                timestamp -= self.init_timestamp[cam]
                init_timestamp_set = True
                self.init_groupframe_id = int(groupframe_id)


            
            h4d_frame = H4DFrame(groupframe_id, frame_id, color_img, depth_img, timestamp)
            self.cameras[cam].append(h4d_frame)
            # self.cameras[cam]
        
        self.num_of_frames = len(self.cameras[cam])
