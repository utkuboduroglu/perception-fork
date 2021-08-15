import sys
# this is required to load the submodule library
sys.path.insert(1, './submodules/pytorch-YOLOv4/')

# Pycharm warns for this but it executes
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet

from process.iparse import get_args

"""hyper parameters"""
# disable CUDA for normal computers,
# REMEMBER TO ENABLE THIS FOR THE CAR
use_cuda = False

def detect_cv2_camera(cfgfile, weightfile, v_device):
    import cv2
    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))

    if use_cuda:
        m.cuda()

    cap = cv2.VideoCapture(v_device)
    # cap = cv2.VideoCapture("./test.mp4")

    # sets width/height
    cap.set(3, 832)
    cap.set(4, 416)
    print("Starting the YOLO loop...")

    # we do this because we know the dataset is coco,
    # replace this with our own once we can generate datasets
    class_names = load_class_names('data/coco.names')

    while True:
        ret, img = cap.read()
        sized = cv2.resize(img, (m.width, m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = time.time()
        print('Predicted in %f seconds.' % (finish - start))

        result_img = plot_boxes_cv2(img, boxes[0], savename=None, class_names=class_names)

        cv2.imshow('Yolo demo', result_img)
        cv2.waitKey(1)

    cap.release()

if __name__ == '__main__':
    args = get_args()
    detect_cv2_camera(args.cfgfile, args.weightfile, args.v_device)
