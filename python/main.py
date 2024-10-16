import asyncio
import nidaqmx
from components.input import Input
# from components.outout import Output


# 変数
t_max = 10
sampling_rate = 0.1
user_name = 'sasaki'
filename = 'test'


async def run(t_max: float, sampling_rate: float, user_name: str, filename: str):
  # インスタンス化
  input = Input(t_max, sampling_rate, user_name, filename)
  print('インスタンス化完了')

  # タスクを作成
  task = nidaqmx.Task()
  print(type(task))

  # 入力の取り込み
  task, data = input.input(task)
  print(data)

  # タスクの終了
  task.close()

  return


if __name__ == '__main__':
  asyncio.run(run())