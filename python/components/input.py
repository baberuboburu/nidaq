import nidaqmx
from nidaqmx.task import Task
import time
import datetime
import os
import pandas as pd
from ctypes import windll




class Input():
  def __init__(self, n: int, sampling_rate: float, user_name: str, filename: str):
    '''
    n: 測定点数
    sampling_rate: サンプリング間隔
    user_name: 実験者(ファイル保存時に利用)
    filename: 保存するファイル名
    '''
    self.n = n
    self.sampling_rate = sampling_rate
    self.user_name = user_name
    self.filename = filename


  async def input(self, task: Task):
    data = []

    # OSのタイマー精度を1ミリ秒に変更
    windll.winmm.timeBeginPeriod(1)

    # タスクを開始
    task.start()

    # データの取り込み(入力)
    start_time = time.perf_counter()
    for _ in range(self.n):
      value = task.read()
      now = datetime.datetime.now()
      step_time = time.perf_counter()
      value[0:0] = [now, step_time - start_time]
      data.append(value)

      # サンプリング間隔を開ける
      time.sleep(self.sampling_rate)
    
    # タスクを停止
    task.stop()

    # OSのタイマー精度をもとに戻す
    windll.winmm.timeEndPeriod(1)
    

import pandas as pd
import os

class Input:
  def __init__(self, user_name: str, filename: str):
    self.user_name = user_name
    self.filename = filename
    
    
  def save(self, data, columns):
    # 保存先ディレクトリを作成
    folder_path = f'C:/Users/{self.user_name}/Desktop/savedata/{self.user_name}'
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    # データをpandas DataFrameに変換して保存
    df = pd.DataFrame(data, columns=columns)
    file_path = f'{folder_path}/{self.filename}.csv'
    df.to_csv(file_path, index=False)
    print(f'Data saved to {file_path}')
