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
  print(len(output_vols))

  # タスクを作成
  task_ai = nidaqmx.Task()
  task_ao = nidaqmx.Task()

  # 電圧の印加, 出力の取り込み
  task, data = await daq.main(task_ai, task_ao, output_vols)
  print(data)

  # タスクの終了
  task.close()

  columns = ['time', 'ref_time', 'output_0']
  plot = Plot(data, columns)
  plot.plot()

  return


if __name__ == '__main__':
  asyncio.run(run(func, t_max, sampling_rate, username, filename))