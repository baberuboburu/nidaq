import asyncio
import nidaqmx
from components.daq import Daq
from components.function import Function
from components.plot import Plot


# 変数
func1 = 'dc'  # "dc", "sinx", "cosx", "triangle", "sawtooth"
func2 = 'dc'
t_max = 10000
sampling_rate = 100
frequency = 1
username = 'sasaki'
filename = 'test'
output_num = 2
input_num = 1


async def run(t_max: float, sampling_rate: float, username: str, filename: str):
  # 定数
  n = int(t_max / sampling_rate)
  print(n)

  # インスタンス化
  daq = Daq(n, sampling_rate, username, filename)
  function = Function(n)
  plot = Plot(username, filename)

  # volsリストを動的に生成
  # triangle = await function.main(func1, amplitude=1.0, frequency=frequency, sampling_rate=sampling_rate)
  dc1 = await function.main(func1, vol=1.5)
  dc2 = await function.main(func2, vol=0.5)
  output_vols = [dc1, dc2]

  # タスクを作成
  task_ai = nidaqmx.Task()
  task_ao = nidaqmx.Task()

  # 電圧の印加, 出力の取り込み
  task_ai, task_ao, df = await daq.main(task_ai, task_ao, output_vols)
  print(df.head(3))

  # タスクの終了
  task_ai.close()
  task_ao.close()

  columns = ['time', 'ref_time', ] + [f"voltage_ai{i}" for i in range(1)] + [f"voltage_ao{i}" for i in range(2)]

  return


if __name__ == '__main__':
  asyncio.run(run(t_max, sampling_rate, username, filename))




'''
【進捗】
・基本的なコーディングが完了した。
・出力の接続テストを完了した。

【残り作業】
・入力のデバイスとチャンネルの設定を行う。
  - ChatGPTにマニュアルを読み込ませ、試行錯誤する
  
【これをみて作業を続ける】
・nidaqmx関連
https://chatgpt.com/c/670f71df-5ec4-800e-af6c-8d83a86d35c3
・score関連
https://chatgpt.com/c/6715e2aa-5bc4-800e-9097-e4af0a67d135
・
'''