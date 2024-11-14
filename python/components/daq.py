import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx.task import Task
import time
import datetime
from ctypes import windll
from typing import Tuple
import pandas as pd
import os
from components.optimize import Optimize


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
    self.file_path = os.path.join(f'./img/{username}', filename)


  async def main(self, task_ai: Task, task_ao: Task, outputs: list[float]) -> Tuple[Task, Task, pd.DataFrame]:
    # 初期値
    data = []
    optimize = Optimize()

    # タスクにデバイス(PXI1Slot3)のチャンネル(ai0~ai15, ao0~ao1)を追加
    task_ai.ai_channels.add_ai_voltage_chan("PXI1Slot3/ai0:15")
    # task_ao.ao_channels.add_ao_voltage_chan("PXI1Slot3/ao0:1")
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
      task_ao.write(outputs[k])

      # 電流値を読み取り
      data_k = task_ai.read()

      # タイムスタンプを作成
      now = datetime.datetime.now()
      step_time = time.perf_counter()
      data_k[0:0] = [now, step_time - start_time]
      data.append(data_k)

      # # サンプリング間隔を開ける
      # time.sleep(self.sampling_rate)
    
    # タスクを停止
    task_ai.stop()
    task_ao.stop()

    # OSのタイマー精度をもとに戻す
    windll.winmm.timeEndPeriod(1)

    # dataの形式を変換する
    df = pd.DataFrame(data, columns=["timestamp", "elapsed_time"] + [f"voltage_{i}" for i in range(16)])
    outputs_df = pd.DataFrame(outputs, columns=["output_voltage"])

    ''' ここから '''
    # 入力(まずは2つ)を解析する
    sorted_columns = optimize.main(df, 'nonlinearity')
    optimized_column = sorted_columns[0]
    
    ''' ここまで '''

    # dataにoutputsを列として追加
    df = pd.concat([df, outputs_df], axis=1)

    # データをcsvに保存する
    await self.save_data(df)

    return task_ai, task_ao, df
  

  async def save_data(self, data: pd.DataFrame) -> None:
    os.makedirs(os.path.dirname(self.dir_path), exist_ok=True)
    data.to_csv(self.file_path, index=False)
    return



# """ここから"""

# Tstop = 10 # 測定終了時間
# St = 0.1 # サンプリング間隔
# Username = "matsuo" # 実験者名
# Filename = "001" # 保存するファイル名(重要)

# """ここまで"""

# print("Start")

# N = int(Tstop/St)
# data = []

# task = nidaqmx.Task()
# task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:15")

# windll.winmm.timeBeginPeriod(1) # OSのタイマー精度を1ミリ秒に変更

# task.start()
# start_time = time.perf_counter()

# for k in range(N):
#   value = task.read()
#   value[0:0]=[datetime.datetime.now(), time.perf_counter()-start_time]
#   data = data.append(value)
#   time.sleep(St)

# task.stop()
# task.close()

# windll.winmm.timeEndPeriod(1) # OSのタイマー精度をもとに戻す

# df = pd.DataFrame(data, columns=["時刻", "経過時間", "output1", "output2", "output3", "output4", "output5", "output6", "output7", "output8", "output9", "output10", "output11", "output12", "output13", "output14", "output15"])

# print(df)

# #保存先フォルダ作成
# def make_folder(folder_name):
#     if not os.path.exists(folder_name):
#         os.mkdir(folder_name)

# def dt_today():
#     today = datetime.date.today()
#     yymmdd = '{:%y%m%d}'.format(today)
#     return yymmdd

# make_folder('C:\\Users\\matsumoto\\Desktop\\savadata\\{}'.format(Username))
# make_folder('C:\\Users\\matsumoto\\Desktop\\savadata\\{}\\{}'.format(Username, dt_today()))


# #ファイル保存
# df.to_csv('C:\\Users\\matsumoto\\Desktop\\savadata\\{}\\{}\\{}.csv'.format(Username, dt_today(), Filename), index=False)

# #グラフ描画
# fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=200, tight_layout=True)
# ax.plot(df["測定時間"], df["output1"])
# ax.plot(df["測定時間"], df["output2"])
# ax.set_title("V-t graph")
# ax.set_xlabel("Time / s")
# ax.set_ylabel("Voltage / V")
# ax.grid()
# plt.show()

# print("Finished")