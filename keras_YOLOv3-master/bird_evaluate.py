"""
Evaluate the YOLO model for your own dataset.
"""

import colorsys
import os
from timeit import default_timer as timer

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image, ImageFont, ImageDraw

from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3.utils import letterbox_image
import os
from keras.utils import multi_gpu_model
     

class YOLO(object):
    # Change parameters here for your application
    _defaults = {
        "model_path": 'logs/20200305/ep060-loss95.325-val_loss91.687.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/bird_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults) # set up default values
        self.__dict__.update(kwargs) # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        print('num_anchors : {}  num_classes : {} '.format(num_anchors, num_classes))
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)
        print("boxes : ", boxes)
        print("scores : ", scores)
        print("classes : ", classes)

        return boxes, scores, classes

    def detect_image(self, image):
        import cv2
        start = timer()

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')

        print(image_data.shape)
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        print("out_boxes : ", out_boxes.shape, type(out_boxes), out_boxes)
        print("out_scores : ", type(out_scores), out_scores)
        print("out_classes : ", out_classes.shape, type(out_classes), out_classes)
        
        # Change y axis data
        pred_box_ch = np.zeros((out_boxes.shape[0], 5), 'int32')

        print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

        font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                    size=np.floor(2e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 500

        for i, c in list(enumerate(out_classes)):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            print(label, (top, left), (bottom, right))
            # Change y axis data
            pred_box_ch[i, 0] = left
            pred_box_ch[i, 1] = top
            pred_box_ch[i, 2] = right
            pred_box_ch[i, 3] = bottom
            pred_box_ch[i, 4] = c

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self.colors[c])
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)
            del draw

        end = timer()
        print(end - start)
        return image, pred_box_ch, out_scores

    def close_session(self):
        self.sess.close()

def compute_iou(box, boxes, box_area, boxes_area):
    """Calculates IoU of the given box with the array of the given boxes.
    box: 1D vector [y1, x1, y2, x2]
    boxes: [boxes_count, (y1, x1, y2, x2)]
    box_area: float. the area of 'box'
    boxes_area: array of length boxes_count.

    Note: the areas are passed in rather than calculated here for
    efficiency. Calculate once in the caller to avoid duplicate work.
    """
    # Calculate intersection areas
    y1 = np.maximum(box[0], boxes[:, 0])
    y2 = np.minimum(box[2], boxes[:, 2])
    x1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[3], boxes[:, 3])
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[:] - intersection[:]
    iou = intersection / union
    return iou

def compute_overlaps(boxes1, boxes2):
    """Computes IoU overlaps between two sets of boxes.
    boxes1, boxes2: [N, (y1, x1, y2, x2)].

    For better performance, pass the largest set first and the smaller second.
    """
    # Areas of anchors and GT boxes
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    # Compute overlaps to generate matrix [boxes1 count, boxes2 count]
    # Each cell contains the IoU value.
    overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
    for i in range(overlaps.shape[1]):
        box2 = boxes2[i]
        overlaps[:, i] = compute_iou(box2, boxes1, area2[i], area1)
    return overlaps

def compute_recall(pred_boxes, gt_boxes, iou_threshold):
    """Compute the recall at the given IoU threshold. It's an indication
    of how many GT boxes were found by the given prediction boxes.

    pred_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    gt_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    """
    # Measure overlaps
    overlaps = compute_overlaps(pred_boxes, gt_boxes)
    print(overlaps)
    iou_max = np.max(overlaps, axis=1)
    iou_argmax = np.argmax(overlaps, axis=1)
    positive_ids = np.where(iou_max >= iou_threshold)[0]
    matched_gt_boxes = iou_argmax[positive_ids]

    recall = len(set(matched_gt_boxes)) / gt_boxes.shape[0]
    return recall, positive_ids

def compute_matches(gt_boxes_classes, pred_boxes_classes, iou_threshold):
    """Finds matches between prediction and ground truth instances.

    Returns:
        gt_match: 1-D array. For each GT box it has the index of the matched
                  predicted box.
        pred_match: 1-D array. For each predicted box, it has the index of
                    the matched ground truth box.
    """
    print('gt_boxes_classes: ', gt_boxes_classes, '/', gt_boxes_classes.shape)

    # Loop through predictions and find matching ground truth boxes
    match_count = 0

    # Compute IoU overlaps [pred_masks, gt_masks]
    overlaps = compute_overlaps(pred_boxes_classes, gt_boxes_classes)

    pred_match = -1 * np.ones([pred_boxes_classes.shape[0]])
    gt_match = -1 * np.ones([gt_boxes_classes.shape[0]])
    for i in range(len(pred_boxes_classes)):
        # Find best matching ground truth box
        # 1. Sort matches by score
        sorted_ixs = np.argsort(overlaps[i])[::-1]
        # 2. Find the match
        for j in sorted_ixs:
            # If ground truth box is already matched, go to next one
            if gt_match[j] > -1:
                continue
            # If we reach IoU smaller than the threshold, end the loop
            iou = overlaps[i, j]
            if iou < iou_threshold:
                break
            # Do we have a match?
            if pred_boxes_classes[i, 4] == gt_boxes_classes[j, 4]:
                match_count += 1
                gt_match[j] = i
                pred_match[i] = j
                break
    print("gt_match: {}\n pred_match: {}\n overlaps: {}\n match_count: {}".format(gt_match, pred_match, overlaps, match_count))

    return gt_match, pred_match

def compute_ap(gt_boxes_classes, pred_boxes_classes, iou_threshold):
    """Compute Average Precision at a set IoU threshold (default 0.5).

    Returns:
    mAP: Mean Average Precision
    precisions: List of precisions at different class score thresholds.
    recalls: List of recall values at different class score thresholds.
    overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    TP = 0
    FP = 0
    FN = 0
    # Get matches and overlaps
    gt_match, pred_match = compute_matches(gt_boxes_classes, pred_boxes_classes, iou_threshold)

    for i in range(len(gt_match)):
        if gt_match[i] != -1:
            TP += 1
        else:
            FN += 1
    for i in range(len(pred_match)):
        if pred_match[i] == -1:
            FP += 1    

    print("TP: {} FN: {} FP: {}".format(TP, FN, FP))

    # Compute precision and recall at each prediction box step
    precisions = np.cumsum(pred_match > -1) / (np.arange(len(pred_match)) + 1)
    recalls = np.cumsum(pred_match > -1).astype(np.float32) / len(gt_match)
    # print("precisions: {}\nrecalls: {}".format(precisions, recalls))
    # Pad with start and end values to simplify the math
    precisions = np.concatenate([[0], precisions, [0]])
    recalls = np.concatenate([[0], recalls, [1]])
    # print("precisions: {}\nrecalls: {}".format(precisions, recalls))

    # Ensure precision values decrease but don't increase. This way, the
    # precision value at each recall threshold is the maximum it can be
    # for all following recall thresholds, as specified by the VOC paper.
    for i in range(len(precisions) - 2, -1, -1):
        precisions[i] = np.maximum(precisions[i], precisions[i + 1])
    # print("precisions: ", precisions)
    # Compute mean AP over recall range
    indices = np.where(recalls[:-1] != recalls[1:])[0] + 1
    # print(indices, type(indices))
    mAP = np.sum((recalls[indices] - recalls[indices - 1]) *
                 precisions[indices])

    return mAP, TP, FN, FP

def _main(YOLO):
    # Set proper IOU for your application!!!
    IOU = 0.1

    # You can change the folder path
    dir_path = '/home/nchupmml705/keras_YOLOv3/dataset/val/'
    annotation_path = 'dataset/annotation_val/annotation_val.txt'
    # Read annotation
    with open(annotation_path) as f:
        anno_lines = f.readlines()
    # Read and sort images
    lines = os.listdir(dir_path)
    lines.sort()
    print(lines[:-1])
    # Prepare for calculate mAP
    APs = []
    ARs = []
    TPs = []
    FNs = []
    FPs = []

    try:
        for i,line in enumerate(lines[:-1]):
            # Detect image
            print(i, line)
            image = Image.open(dir_path+line)
            r_image, pred_box_ch, out_scores = YOLO.detect_image(image)
            # Svae directory of detected image
            r_image.save("/home/nchupmml705/keras_YOLOv3/temp_image/{}".format(line), 'JPEG')
            # Calculate precision, recall and AP
            anno_line = anno_lines[i].split()
            gt_box = np.array([np.array(list(map(int,gt_box.split(',')))) for gt_box in anno_line[1:]])

            recall, positive_ids = compute_recall(pred_box_ch, gt_box, iou_threshold=IOU)
            AP, TP, FN, FP = compute_ap(gt_box, pred_box_ch, iou_threshold=IOU)
            print("recall:{}  positive_ids: {}".format(recall, positive_ids))
            print("AP:{}".format(AP))

            APs.append(AP)
            ARs.append(recall)
            TPs.append(TP)
            FNs.append(FN)
            FPs.append(FP)
            
        print(len(ARs))
        print("AR @ IoU=", IOU, ":", np.mean(ARs))
        print("TP: {} FN: {} FP: {}".format(np.sum(TPs), np.sum(FNs), np.sum(FPs)))
        print("mAP @ IoU=", IOU, ":", np.mean(APs))

        YOLO.close_session()
    except:
        YOLO.close_session()

if __name__ == '__main__':
    _main(YOLO())