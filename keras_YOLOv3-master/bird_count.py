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
    # Change parameters here for your application!!!
    _defaults = {
        "model_path": 'logs/20200305/ep060-loss95.325-val_loss91.687.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/bird_classes.txt',
        "score" : 0.15,
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
        count = len(out_classes)
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
        return image, count

    def close_session(self):
        self.sess.close()


def _main(YOLO):

    # You can change the folder path!!!
    dir_path = 'C:/Users/nchupmml705/PycharmProjects/keras_YOLOv3/dataset/test/'
    # Read and sort images
    lines = os.listdir(dir_path)
    lines.sort()
    # print(lines[:-1])

    #Create and open file.txt for laser time log!!!
    filelog = open("bird_num/birdnumber20190317.txt", "w")

    count = 0
    bird_count_per_hour = 0

    try:
        for i,line in enumerate(lines):
            # Detect image
            print(i, line)
            image = Image.open(dir_path+line)
            r_image, bird_count = YOLO.detect_image(image)
            # Svae directory of detected image
            r_image.save("/home/nchupmml705/keras_YOLOv3/temp_image/{}".format(line), 'JPEG')
            # Svae directory of detected image!!!
            r_image.save("C:/Users/nchupmml705/PycharmProjects/keras_YOLOv3/temp_image/{}".format(line), 'JPEG')
            # Calculate bird numbers
            print("YOLO bird number: ", bird_count)
            # Parameters mean : predict_box -> true positive -> total birds
            true_bird_number = int(bird_count * 0.684 * 3.663) # precision:1278/1867=0.684 , recall:1278/4673=0.273 
            print("True bird number: ", true_bird_number)
            bird_count_per_hour += true_bird_number

            if i%60 == 59:
                count += 1
                print("{} hour".format(count))
                #Log bird number per hour to lasertime.txt
                filelog.write(str(count))
                filelog.write(" bird_number: ")
                filelog.write(str(bird_count_per_hour))
                filelog.write("\n")
                bird_count_per_hour = 0

        YOLO.close_session()
    except:
        YOLO.close_session()

if __name__ == '__main__':
    _main(YOLO())