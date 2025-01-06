import asyncio
import nidaqmx
from components.daq import Daq
from components.function import Function


# 変数
func = 'triangle'  # "dc", "sinx", "cosx", "triangle", "sawtooth"
t_max = 10000
sampling_rate = 10
frequency = 0.1
amplitude = 3
n_cycle = 1
username = 'sasaki'
date = '20250106'
filename = f'{func}{amplitude * 1000}mV'
output_num = 1
input_num = 7


async def run(t_max: float, sampling_rate: float, username: str, filename: str):
  # 定数
  n = int(t_max / sampling_rate)
  print(n)

  # インスタンス化
  dir_name = f'{username}/{date}/{func}{amplitude * 1000}mV'
  daq = Daq(n, sampling_rate, dir_name, filename)
  function = Function(n)

  # volsリストを動的に生成
  input_function = await function.main(func, amplitude=amplitude)
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