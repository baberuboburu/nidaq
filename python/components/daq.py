import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx.task import Task
import time
import datetime
from ctypes import windll
from typing import Tuple, List
import pandas as pd
import os
from components.optimize import Optimize
from components.plot import Plot


class Daq():
  def __init__(self, n: int, sampling_rate: float, username: str, filename: str):
    '''
    n: 測定点数
    sampling_rate: サンプリング間隔
    username: 実験者(ファイル保存時に利用)
    filename: 保存するファイル名
    '''
    self.n = n
    self.sampling_rate = sampling_rate
    self.username = username
    self.filename = filename
    self.dir_path = f'./csv/{username}'
    self.file_path = os.path.join(self.dir_path, f'{filename}.csv')
  

  async def main(self, func: str, task_ai: Task, task_ao: Task, outputs: List[List[float]], output_num: int, input_num: int) -> Tuple[Task, Task]:
    if func == 'dc':
      task_ai, task_ao = await self.dc(task_ai, task_ao, outputs, output_num, input_num)
    elif func == 'triangle':
      task_ai, task_ao = await self.triangle(task_ai, task_ao, outputs, output_num, input_num)
    
    return task_ai, task_ao


  async def triangle(self, task_ai: Task, task_ao: Task, outputs: List[List[float]], output_num: int, input_num: int) -> Tuple[Task, Task]:
    # 初期値
    data = []
    optimize = Optimize()

    # タスクにデバイス(PXI1Slot3)のチャンネル(ai0~ai15, ao0~ao1)を追加
    if input_num > 1:
      task_ai.ai_channels.add_ai_voltage_chan(f"PXI1Slot3/ai0:{input_num - 1}")
    else:
      task_ai.ai_channels.add_ai_voltage_chan("PXI1Slot3/ai0")

    if output_num > 1:
      task_ao.ao_channels.add_ao_voltage_chan(f"PXI1Slot3/ao0:{output_num - 1}")
    else:
      task_ao.ao_channels.add_ao_voltage_chan("PXI1Slot3/ao0")

    # サンプリングレートを設定
    task_ai.timing.cfg_samp_clk_timing(rate=self.sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)

    # OSのタイマー精度を1ミリ秒に変更
    windll.winmm.timeBeginPeriod(1)

    # タスクの開始
    task_ai.start()
    task_ao.start()

    # データの取り込み
    start_time = time.perf_counter()
    for k in range(self.n):
      # 電圧を印加
      # output_data = [outputs[0][k]]
      output_data = [outputs[i][k] for i in range(output_num)]
      task_ao.write(output_data)

      # 電流値を読み取り
      data_k = task_ai.read()
      if type(data_k) == float:
        data_k = [data_k]

      # タイムスタンプを作成
      now = datetime.datetime.now()
      step_time = time.perf_counter()
      data_k[0:0] = [now, step_time - start_time]
      print(data_k)
      data.append(data_k)
    
    # タスクを停止
    task_ai.stop()
    task_ao.stop()

    # OSのタイマー精度をもとに戻す
    windll.winmm.timeEndPeriod(1)

    # dataの形式を変換する
    inputs_df = pd.DataFrame(data)
    outputs_df = pd.DataFrame(outputs).T

    input_column_names = ["timestamp", "elapsed_time"] + [f"voltage_ai{i}" for i in range(input_num)]
    output_column_names = [f"voltage_ao{i}" for i in range(output_num)]

    inputs_df.columns = input_column_names
    outputs_df.columns = output_column_names
    df = pd.concat([inputs_df, outputs_df], axis=1)

    # IV特性のプロットと保存
    plotter = Plot(self.username)
    plotter.plot_iv_curve(df)

    # 入力(まずは2つ)を解析する
    # sorted_columns = await optimize.main(df, 'nonlinearity')
    # optimized_column = sorted_columns[0]
    # print(f'非線形性が最も高い電極: {optimized_column}')

    # データをcsvに保存する
    await self.save_data(df)

    return task_ai, task_ao
  

  async def save_data(self, data: pd.DataFrame) -> None:
    os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    data.to_csv(self.file_path, index=False)
    return
  

  async def dc(self, task_ai: Task, task_ao: Task, outputs: List[List[float]], output_num: int, input_num: int) -> Tuple[Task, Task]:
    # 初期値
    data = []
    optimize = Optimize()

    # タスクにデバイス(PXI1Slot3)のチャンネル(ai0~ai15, ao0~ao1)を追加
    if input_num > 1:
      task_ai.ai_channels.add_ai_voltage_chan(f"PXI1Slot3/ai0:{input_num - 1}")
    else:
      task_ai.ai_channels.add_ai_voltage_chan("PXI1Slot3/ai0")

    if output_num > 1:
      task_ao.ao_channels.add_ao_voltage_chan(f"PXI1Slot3/ao0:{output_num - 1}")
    else:
      task_ao.ao_channels.add_ao_voltage_chan("PXI1Slot3/ao0")

    # サンプリングレートを設定
    task_ai.timing.cfg_samp_clk_timing(rate=self.sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)

    # OSのタイマー精度を1ミリ秒に変更
    windll.winmm.timeBeginPeriod(1)

    # タスクの開始
    task_ai.start()
    task_ao.start()

    # データの取り込み
    start_time = time.perf_counter()
    for k in range(self.n):
      # 電圧を印加
      # output_data = [outputs[0][k]]
      output_data = [outputs[i][k] for i in range(output_num)]
      task_ao.write(output_data)

      # 電流値を読み取り
      data_k = task_ai.read()
      if type(data_k) == float:
        data_k = [data_k]

      # タイムスタンプを作成
      now = datetime.datetime.now()
      step_time = time.perf_counter()
      data_k[0:0] = [now, step_time - start_time]
      print(data_k)
      data.append(data_k)
    
    # タスクを停止
    task_ai.stop()
    task_ao.stop()

    # OSのタイマー精度をもとに戻す
    windll.winmm.timeEndPeriod(1)

    # dataの形式を変換する
    inputs_df = pd.DataFrame(data)
    outputs_df = pd.DataFrame(outputs).T

    input_column_names = ["timestamp", "elapsed_time"] + [f"voltage_ai{i}" for i in range(input_num)]
    output_column_names = [f"voltage_ao{i}" for i in range(output_num)]

    inputs_df.columns = input_column_names
    outputs_df.columns = output_column_names
    df = pd.concat([inputs_df, outputs_df], axis=1)
    print(df.head(3))

    # IV特性のプロットと保存
    plotter = Plot(self.username)
    plotter.plot_dc(df)

    # # 入力(まずは2つ)を解析する
    # sorted_columns = await optimize.main(df, 'nonlinearity')
    # optimized_column = sorted_columns[0]
    # print(f'非線形性が最も高い電極: {optimized_column}')

    # データをcsvに保存する
    await self.save_data(df)

    return task_ai, task_ao