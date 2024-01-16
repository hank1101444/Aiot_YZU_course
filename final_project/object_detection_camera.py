import cv2
import numpy as np
import tensorflow as tf
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys
sys.path.append('..') 
sys.path.append('../..')
from utils import label_map_util
from utils import visualization_utils as vis_util
import time
import os


class ObjectDetector:
    def __init__(self, camera_type='usb', model_name='ssdlite_mobilenet_v2_coco_2018_05_09'):
        self.camera_type = camera_type
        self.model_name = model_name
        self.load_model()
        self.setup_camera()

    def load_model(self):
        # 加载模型和标签映射等
        CWD_PATH = os.getcwd()
        PATH_TO_CKPT = os.path.join(CWD_PATH, self.model_name, 'frozen_inference_graph.pb')
        PATH_TO_LABELS = os.path.join(CWD_PATH, 'data', 'mscoco_label_map.pbtxt')
        NUM_CLASSES = 90

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        self.detection_graph = tf.compat.v1.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.sess = tf.compat.v1.Session(graph=self.detection_graph)

    def setup_camera(self):
        # 设置摄像头
        IM_WIDTH = 300
        IM_HEIGHT = 300

        if self.camera_type == 'picamera':
            self.camera = PiCamera()
            self.camera.resolution = (IM_WIDTH, IM_HEIGHT)
            self.camera.framerate = 10
            self.rawCapture = PiRGBArray(self.camera, size=(IM_WIDTH, IM_HEIGHT))
        elif self.camera_type == 'usb':
            self.camera = cv2.VideoCapture(0, cv2.CAP_V4L)
            if not self.camera.isOpened():
                raise Exception("无法开启摄像头")
            self.camera.set(3, IM_WIDTH)
            self.camera.set(4, IM_HEIGHT)

    def detect_objects(self):
        # 进行物体检测
        if self.camera_type == 'picamera':
            for frame1 in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                frame = np.copy(frame1.array)
                frame.setflags(write=1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_expanded = np.expand_dims(frame_rgb, axis=0)
                self.detect_and_display(frame, frame_expanded)
                self.rawCapture.truncate(0)
        elif self.camera_type == 'usb':
            while True:
                ret, frame = self.camera.read()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_expanded = np.expand_dims(frame_rgb, axis=0)
                self.detect_and_display(frame, frame_expanded)

    def detect_and_display(self, frame, frame_expanded):
        # 检测并显示结果
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_graph.get_tensor_by_name('detection_boxes:0'),
             self.detection_graph.get_tensor_by_name('detection_scores:0'),
             self.detection_graph.get_tensor_by_name('detection_classes:0'),
             self.detection_graph.get_tensor_by_name('num_detections:0')],
            feed_dict={self.detection_graph.get_tensor_by_name('image_tensor:0'): frame_expanded})

        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.8)

        cv2.imshow('Object detector', frame)
        if cv2.waitKey(1) == ord('q'):
            return

    def cleanup(self):
        # 清理资源
        if self.camera_type == 'usb':
            self.camera.release()
        cv2.destroyAllWindows()
        self.sess.close()

# 使用示例
if __name__ == "__main__":
    detector = ObjectDetector(camera_type='usb')  # 可以改为 'picamera'
    try:
        detector.detect_objects()
    except KeyboardInterrupt:
        detector.cleanup()
