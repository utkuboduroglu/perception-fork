import sys
# this is required to load the submodule library
sys.path.insert(1, './submodules/pytorch-YOLOv4/')

# Pycharm warns for this but it executes
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet

from process.iparse import get_args
from process.image import plot_boxes_cv2

# Default Hyperparameters
## Use CUDA for GPU acceleration, enable this for the car itself
use_cuda = False
## Draw OpenCV graphics, disabling may give FPS boost
draw_graphics = True

def detect_cv2_camera(cfgfile, weightfile, v_device, namefile):
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
    class_names = load_class_names(namefile)

    while True:
        ret, img = cap.read()
        sized = cv2.resize(img, (m.width, m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = time.time()
        print('Predicted in %f seconds.' % (finish - start))

        if draw_graphics:
            result_img = plot_boxes_cv2(img, boxes[0], savename=None, class_names=class_names)
            # display FPS
            fps_label = str(int(1/(finish-start)))
            text_size, _ = cv2.getTextSize(fps_label, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 1)
            tx, ty = text_size
            result_img = cv2.rectangle(result_img, (20, 60-ty), (20+tx, 60), (0,0,0), -1)
            result_img = cv2.putText(result_img, str(int(1/(finish-start))),
                                     (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 1)

            cv2.imshow('YOLOv4 prediction', result_img)
            cv2.waitKey(1)

    cap.release()

if __name__ == '__main__':
    args = get_args()
    # we set the hyperparameters according to our cmdline arguments
    use_cuda = args.cuda
    draw_graphics = args.draw

    detect_cv2_camera(args.cfgfile, args.weightfile, args.v_device, args.namefile)
