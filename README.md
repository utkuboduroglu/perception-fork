# METU Racing Driverless Perception pipeline
This is the official Github repository for the perception pipeline of the METU Racing's Driverless project. Some of the primary goals of this pipeline is solving for object detection through visual and LIDAR data.

## Notes
* For a quickstart on `git`, check out [using `git`](https://htmlpreview.github.io/?https://github.com/utkuboduroglu/dev-toolkit-docs/blob/master/using-git/README.html).
* For a reference on writing proper commit messages, check out [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).


## How to predict
We rely on 2 submodules for running our YOLOv4 predictions: `Darknet` and `Tianxiaomo/Pytorch-YOLOv4`. Here are the use cases for these modules:

* `Darknet` for general training on datasets. We convert our dataset to the Darknet format and train. This can be done on any local machine, but for convenience and performance, should be done on cloud systems like Google Colab and/or Paperspace.
* `Tianxiaomo YOLOv4` for the base implementation of Darknet on Python. We use the code as a draft for our own program and compile with CUDA and OpenCV. We use the webcam code for live predictions, but do note that running the prediction code on most machines is slow.
* For our specialized use, we should convert Tianxiaomo's code into a module and import it into our code (at first). We don't need to modify Darknet, it's only for the training process of the dataset.
    - For speed improvements, we can use datasets with small amounts of labels and use yolov4-tiny. The method for processing datasets is present in [Darknet's github page](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects).

## Building a Dockerfile for model training
Here are some guidelines for our Dockerfile to be used during training:

* We should use Ubuntu as a base image.
* We should build Darknet from scratch, we need to be able to use OpenCV and CUDA during the training process to improve our times.
* If we gain access to FSOCO, we can use that dataset directly. If not, we need to find a way to import our datasets into the Dockerfile as well.
* We need to collect metrics during training to be able to determine the best model possible and evaluate fitness etc., so find a way to collect said metrics off of training with Darknet.

## Resources
The following items are resources we chose to follow during the development process. This list will be updated periodically.

* [AMZ Driverless: The Full Autonomous Racing System](https://arxiv.org/abs/1905.05150)
* [The Complete Self-Driving Car Course - Applied Deep Learning](https://www.udemy.com/course/applied-deep-learningtm-the-complete-self-driving-car-course/)
* [OpenCV Python Tutorial For Beginners ](https://www.youtube.com/playlist?list=PLS1QulWo1RIa7D1O6skqDQ-JZ1GGHKK-K)
* [Robotics: Perception](https://www.coursera.org/learn/robotics-perception)
* [Self-Driving Cars Specialization](https://www.coursera.org/specializations/self-driving-cars)
* [Introduction to Computer Vision](https://classroom.udacity.com/courses/ud810)
* [Getting Started with LIDAR](https://www.youtube.com/watch?v=VhbFbxyOI1k)
* [Labeling Ground Truth for Object Detection](https://www.youtube.com/watch?v=ow_B_30WU1s&list=PLn8PRpmsu08qNhzC219pLDcfIN8dHJ2WF)
* [Deep Learning with Python](http://libgen.rs/book/index.php?md5=584B39E75A5B9E072467AFD6A684D0FB)
* [Hands-on Machine Learning with Scikit-Learn and Tensorflow](https://github.com/ageron/handson-ml)
