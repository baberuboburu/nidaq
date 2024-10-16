import nidaqmx
from nidaq.task import Task
import time
import datetime
from ctypes import windll
from typing import Tuple


class Daq():
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


  async def main(self, task: Task, outputs: list[float]) -> Tuple[Task, list[str]]:
    data = []

    # タスクにデバイス(cDAQ1Mod1)のチャンネル(ai0~ai15)を追加
    # task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:15")
    task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")

    # OSのタイマー精度を1ミリ秒に変更
    windll.winmm.timeBeginPeriod(1)

    # タスクを開始
    task.start()

    # データの取り込み
    start_time = time.perf_counter()
    for k in range(self.n):
      # 電圧を印加
      task.write(outputs[k])

      # 電流値を読み取り
      data_k = task.read()

      # タイムスタンプを作成
      now = datetime.datetime.now()
      step_time = time.perf_counter()
      data_k[0:0] = [now, step_time - start_time]
      data.append(data_k)

      # サンプリング間隔を開ける
      time.sleep(self.sampling_rate)
    
    # タスクを停止
    task.stop()

    # OSのタイマー精度をもとに戻す
    windll.winmm.timeEndPeriod(1)
    
    return task, data



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