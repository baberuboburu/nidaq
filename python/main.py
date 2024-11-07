import asyncio
import nidaqmx
from components.daq import Daq
from components.function import Function
from components.plot import Plot


# 変数
func = 'dc'  # "dc", "sinx", "cosx", "triagle", "sawtooth"
t_max = 10
sampling_rate = 0.1
username = 'sasaki'
filename = 'test'


async def run(func: str, t_max: float, sampling_rate: float, username: str, filename: str):
  # 定数
  n = int(t_max / sampling_rate)

  # インスタンス化
  daq = Daq(n, sampling_rate, username, filename)
  function = Function(n)
  plot = Plot(username, filename)

  # 出力電圧の定義
  output_vols = await function.main(func, vol=0.5)

  # タスクを作成
  task_ai = nidaqmx.Task()
  task_ao = nidaqmx.Task()

  # 電圧の印加, 出力の取り込み
  task_ai, task_ao, df = await daq.main(task_ai, task_ao, output_vols)
  print(df.head(3))

  # タスクの終了
  task_ai.close()
  task_ao.close()

  columns = ['time', 'ref_time', ] + [f"voltage_{i}" for i in range(16)] + ['output_0']

  plot = Plot(username, filename)
  plot.plot(df, columns)

  return


if __name__ == '__main__':
  asyncio.run(run(func, t_max, sampling_rate, username, filename))



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