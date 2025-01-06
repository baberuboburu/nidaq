import nidaqmx
from components.daq import Daq
from components.function import Function


async def one_input_multi_outputs(func: str, t_max: int, sampling_rate: float, frequency: float, n_cycle: int, amplitude: float, username: str, date: str, filename: str, output_num: int, input_num: int):
  # 定数
  n = int(t_max / sampling_rate)
  print(n)

  # インスタンス化
  dir_name = f'{username}/{date}/{func}{amplitude * 1000}mV'
  daq = Daq(n, sampling_rate, dir_name, filename)
  function = Function(n)

  # volsリストを動的に生成
  input_function = await function.main(func, amplitude=amplitude, n_cycle=n_cycle)
  output_vols = [input_function]

  # タスクを作成
  task_ai = nidaqmx.Task()
  task_ao = nidaqmx.Task()

  # 電圧の印加, 出力の取り込み
  task_ai, task_ao = await daq.main(func, task_ai, task_ao, output_vols, output_num, input_num)

  # タスクの終了
  task_ai.close()
  task_ao.close()

  return