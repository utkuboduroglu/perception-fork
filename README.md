# METU Racing Driverless Perception pipeline
This is the official Github repository for the perception pipeline of the METU Racing's Driverless project. Some of the primary goals of this pipeline is solving for object detection through visual and LIDAR data.

## Notes
* For a quickstart on `git`, check out [using `git`](https://htmlpreview.github.io/?https://github.com/utkuboduroglu/dev-toolkit-docs/blob/master/using-git/README.html).
* For a reference on writing proper commit messages, check out [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).
* Export the environment variable `DRVLSS_PERCEPTION_PATH` for easier reference to relative paths in our program.
* `bag_to_images.py` is an external tool that helps extract images from rosbags. It can (and should) be used to extract datasets from rosbags we come across (like EUFS or AMZ Driverless' datasets) and prepare a dataset.
* For training on Colab, check out [the Jupyter notebook for training yolov4](https://gist.github.com/utkuboduroglu/bc5eaac95062f4f28db553f2b8fe0caf)
* For creating Darknet configs & additional files, check out [AlexeyAB's Darknet repo](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)

## How to predict
We rely on 2 submodules for running our YOLOv4 predictions: `Darknet` and `Tianxiaomo/Pytorch-YOLOv4`. Here are the use cases for these modules:

* `Darknet` for general training on datasets. We convert our dataset to the Darknet format and train. This can be done on any local machine, but for convenience and performance, should be done on cloud systems like Google Colab and/or Paperspace.
    - As an additional note, Paperspace does not generally allow for Darknet training, but Colab does; please check the section for training on Google Colab for more details.
* `Tianxiaomo YOLOv4` for the base implementation of Darknet on Python. We use the code as a draft for our own program and compile with CUDA and OpenCV. We use the webcam code for live predictions, but do note that running the prediction code on most machines is slow.

## Training our dataset on Google Colab
The whole process of training our dataset can be done on Google Colab, without needing additional hardware or subscriptions etc. The process can be split into two steps: preparing the dataset and training.

1. For preparing our dataset, follow the steps provided by [Darknet's github page](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects). The main steps to follow are creating the `yolo-*.cfg` file, `obj.data` file and `obj.names` file. Furthermore, the dataset needs to be prepared in a special way that each training, validation and testing subset needs to be split into its own subfolder, and each image must be accompanied with a text file with the same name containing the annotation data of the image. Finally, for each subset, there must be a text file specifying the absolute paths of the image files in the subset. These can be made as diverse as possible as creating different permutations of data may be used for cross-validation.
1. After the dataset is prepared, it must be uploaded to Google Drive for the training process. The model training folder must contain the appropriate folders for an easier workflow, specifically: a `cfg` folder for containing the `yolo-*.cfg` files, a `data` folder for containing our training data, our files `obj.data`, `obj.names`, `train-*.txt`, `valid-*.txt`, `test-*.txt`, and a `backup` folder for storing our pre-weights and weights files. After such a directory hierarchy is enforced, one can follow the steps provided in [our Colab train notebook](https://gist.github.com/utkuboduroglu/bc5eaac95062f4f28db553f2b8fe0caf) to train the model. Roughly, this notebook sets up the Drive directory, compiles Darknet for usage and starts training the model. For continued training, the Colab window must remain opened and monitored periodically to prevent timing out. The final output is a `*.weights` file, stored in the `backup` folder.
1. After training is complete, we only need to retrieve the `yolo-*.cfg` file, the `obj.data`, `obj.names` files and the `yolo-*.weights` files to plug into `predict.py`.

## Environment variables
Our codebase has a lot of elements, and for the sake of preserving generality, we have to refrain from using absolute paths and/or relative paths inside our codebase. Instead, we should use environment variables so that we can keep our code portable. Here are some environment variables that we should set:

* `DRVLSS_PERCEPTION_PATH`: The root directory for the perception pipeline. Some of our code requires that this variable be set to run.

## TODO
* Remove save to file features from the code and add it as a final command in predict.py

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
