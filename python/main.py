import asyncio
from dev.one_input_multi_outputs import one_input_multi_outputs
from dev.multi_inputs_one_output import multi_inputs_one_output


# 1入力他出力
func = 'triangle'   # "dc", "sinx", "cosx", "triangle", "sawtooth"
amplitude = 3       # sinやtriangleの振幅, DCの一定の電圧値
frequency = None    # sinやcosの周波数
n_cycle = 1         # triangleを何周期出力するか
t_max = 10000       # t_max/sampling_rate = n
sampling_rate = 10  # サンプリングレート
output_num = 1      # 入力
input_num = 7       # 出力

# 他入力1出力
funcs = ['triangle', 'dc']  # "dc", "sinx", "cosx", "triangle", "sawtooth"
amplitudes = [1, 1]
frequencies = [0.1, None]
n_cycles = [1, None]
t_max = 10000
sampling_rate = 10
output_num = 2
input_num = 1

# 共通設定
username = 'sasaki'
date = '20250106'
filename = f'{func}{amplitude * 1000}mV'


async def one_input():
  await one_input_multi_outputs(func, t_max, sampling_rate, frequency, n_cycle, amplitude, username, date, filename, output_num, input_num)
  return


async def multi_inputs():
  await multi_inputs_one_output(func, t_max, sampling_rate, frequency, n_cycle, amplitude, username, date, filename, output_num, input_num)
  return


if __name__ == '__main__':
  asyncio.run(one_input())
  # asyncio.run(multi_inputs())




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