# Class definition for predictors
from abc import ABC, abstractmethod

class Predictor(ABC):
    @abstractmethod
    def init_network(self):
        pass

    def __init__(self, cfg="", weight="", name="", use_cuda=False, draw_graphics=True):
        self.cfgfile = cfg
        self.weightfile = weight
        self.namefile = name
        self.use_cuda = use_cuda
        self.draw_graphics = draw_graphics

        self.init_network()

    # although not specified here, our predictors only work on devices,
    # so we call the input parameter "data"
    @abstractmethod
    def predict(self, data):
        pass

    # we can specify a lambda here to use for our logging function
    logger = print