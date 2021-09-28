# METU Racing Driverless Perception pipeline
This is the official Github repository for the perception pipeline of the METU Racing's Driverless project. Some of the primary goals of this pipeline is solving for object detection through visual and LIDAR data.

## Notes
* For a quickstart on `git`, check out [using `git`](https://htmlpreview.github.io/?https://github.com/utkuboduroglu/dev-toolkit-docs/blob/master/using-git/README.html).
* For a reference on writing proper commit messages, check out [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).
* Export the environment variable `DRVLSS_PERCEPTION_PATH` for easier reference to relative paths in our program.
* `bag_to_images.py` is an external tool that helps extract images from rosbags. It can (and should) be used to extract datasets from rosbags we come across (like EUFS or AMZ Driverless' datasets) and prepare a dataset.

## Environment variables
Our codebase has a lot of elements, and for the sake of preserving generality, we have to refrain from using absolute paths and/or relative paths inside our codebase. Instead, we should use environment variables so that we can keep our code portable. Here are some environment variables that we should set:

* `DRVLSS_PERCEPTION_PATH`: The root directory for the perception pipeline. Some of our code requires that this variable be set to run.

## The data in use
Currently, all data in use is from rosbags as we have no other source for acquiring datasets/test materials. More specifically, the following are the data we have started using:

* [The Sanderson car park dataset](https://uoe-my.sharepoint.com/:u:/g/personal/eufs_ed_ac_uk/EVAsPplOLPVGpl-fFmNsjs0BA0Iy3KKz7g1xZJFtk4vpSQ?e=89E7EL) from the [Edinburgh University FS team](https://gitlab.com/eufs/datasets).
* [The AMZ Driverless 2017 dataset](https://www.dropbox.com/s/7x75ks6vo2npfv3/AMZ_driverless_2017_dataset.bag.tar.gz?dl=0) from the [AMZ Driverless github page](https://github.com/AMZ-Driverless/fsd-resources#amz_driverless_2017).

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
