# create a camera class and load data in
import argparse

def get_args():
    parser = argparse.ArgumentParser('Test your image or video by trained model.')
    parser.add_argument('--cfg', type=str, default='./cfg/yolov4.cfg',
                        help='path of cfg file', dest='cfgfile')
    parser.add_argument('--weights', type=str,
                        default='./checkpoints/Yolov4_epoch1.pth',
                        help='path of trained model.', dest='weightfile')
    # the default value here kinda breaks things
    parser.add_argument('--img-file', type=str,
                        default='./data/mscoco2017/train2017/190109_180343_00154162.jpg',
                        help='path of your image file.', dest='imgfile')
    # add support for passing in device
    parser.add_argument('--device', type=str,
                        default='/dev/video4',
                        help='path to device.', dest='v_device')
    parser.add_argument('--no-draw', action='store_false', dest='draw')
    args = parser.parse_args()

    return args
