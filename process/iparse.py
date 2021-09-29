# create a camera class and load data in
import argparse

def get_args():
    # make the cfg, weights arguments positional
    parser = argparse.ArgumentParser('Run predictions for a Darknet model.')
    parser.add_argument('--cfg', type=str, default='./cfg/yolov4.cfg',
                        help='Path to the model cfg file.', dest='cfgfile', required=True)
    parser.add_argument('--weights', type=str,
                        default='./checkpoints/Yolov4_epoch1.pth',
                        help='Path of the trained model\'s weights.', dest='weightfile', required=True)
    parser.add_argument('--names', type=str,
                        default='data/coco.names',
                        help='Path for the names of our objects.', dest='namefile', required=True)
    parser.add_argument('--device', type=str, default='/dev/video4',
                        help='Path to device to read video from.', dest='v_device', required=True)
    parser.add_argument('--no-draw', action='store_false', dest='draw',
                        help='Disable drawing OpenCV graphics.')
    parser.add_argument('--cuda', action='store_true', dest='cuda',
                        help='Enable CUDA.')
    args = parser.parse_args()

    return args
