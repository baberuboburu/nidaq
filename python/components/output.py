import nidaqmx
import time
import datetime
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ctypes import windll




class Output():
  def __init__(self):
    '''
    現在のDAQシステムでは、出力に対応できない。
    '''
    pass


  async def output(self):
    return