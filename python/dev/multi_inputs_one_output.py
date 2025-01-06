import nidaqmx
from typing import List
from components.daq import Daq
from components.function import Function


async def multi_inputs_one_output(funcs: List[str], t_max: int, sampling_rate: float, frequencies: List[float], n_cycles: List[int], amplitudes: List[float], username: str, date: str, filename: str, output_num: int, input_num: int):
  # 定数
  dir_name = f'{username}/{date}/{funcs[0]}{amplitudes[0] * 1000}mV'
  n = int(t_max / sampling_rate)
  print(n)

  # インスタンス化
  daq = Daq(n, sampling_rate, dir_name, filename)
  function = Function(n)

  # volsリストを動的に生成
  output_vols = []
  for i in range(output_num):
    func = funcs[i]
    frequency = frequencies[i]
    n_cycle = n_cycles[i]
    amplitude = amplitudes[i]
    input_function = await function.main(func, amplitude=amplitude, n_cycle=n_cycle, frequency=frequency)
    output_vols.append(input_function)

  # タスクを作成
  task_ai = nidaqmx.Task()
  task_ao = nidaqmx.Task()

  # 電圧の印加, 出力の取り込み
  task_ai, task_ao = await daq.main(func, task_ai, task_ao, output_vols, output_num, input_num)

  # タスクの終了
  task_ai.close()
  task_ao.close()

  return