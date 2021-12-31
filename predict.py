import sys
import os
# this is required to load the submodule library
sys.path.insert(1,
                os.path.join(os.environ['DRVLSS_PERCEPTION_PATH'],
                             'submodules/pytorch-YOLOv4/')
                )

# Pycharm warns for this but it executes
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet

from process.iparse import get_args
from process.image import plot_boxes_cv2

import process.metapredict as mpred

# Default Hyperparameters
## Use CUDA for GPU acceleration, enable this for the car itself
use_cuda = False
## Draw OpenCV graphics, disabling may give FPS boost
draw_graphics = True

# instead of just looping in the predict method, initialize the predict method
# with the __init__ call and just run the predictions once
class YOLOv4(mpred.Predictor):
    # specify a logger
    logger = print

    def init_network(self):
        self.m = Darknet(self.cfgfile)

        # does this use a print call?
        self.m.print_network()
        self.m.load_weights(self.weightfile)
        self.logger('Loading weights from %s... Done!' % (self.weightfile))

        if use_cuda:
            self.m.cuda()

        self.logger("Starting the YOLO loop...")

        # we do this because we know the dataset is coco,
        # replace this with our own once we can generate datasets
        self.class_names = load_class_names(self.namefile)

    def predict(self, cap):
        import cv2

        ret, img = cap.read()
        sized = cv2.resize(img, (self.m.width, self.m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(self.m, sized, 0.4, 0.6, self.use_cuda)
        finish = time.time()
        self.logger('Predicted in %f seconds.' % (finish - start))

        if self.draw_graphics:
            result_img = plot_boxes_cv2(img, boxes[0], savename=None, class_names=self.class_names)
            # display FPS
            fps_label = str(int(1/(finish-start)))
            text_size, _ = cv2.getTextSize(fps_label, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 1)
            tx, ty = text_size
            result_img = cv2.rectangle(result_img, (20, 60-ty), (20+tx, 60), (0,0,0), -1)
            result_img = cv2.putText(result_img, str(int(1/(finish-start))),
                                     (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 1)

            cv2.imshow('YOLOv4 prediction', result_img)
            cv2.waitKey(1)

        return boxes


if __name__ == '__main__':
    import cv2
    args = get_args()

    ## Maybe add check for environment variables?
    #if os.environ['DRVLSS_MODEL_PATH']:

    cap = cv2.VideoCapture(args.v_device)
    # cap = cv2.VideoCapture("./test.mp4")

    # sets width/height
    cap.set(3, 832)
    cap.set(4, 416)

    p = YOLOv4(
        args.cfgfile,
        args.weightfile,
        args.namefile,
        use_cuda=args.cuda,
        draw_graphics=args.draw
    )

    while True:
        p.predict(cap)

    cap.release()