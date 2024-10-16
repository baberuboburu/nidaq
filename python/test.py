# import nidaqmx
# import time

# # タスクの作成
# task = nidaqmx.Task()

# # アナログ入力チャンネルの追加 (Dev1のAIチャンネル0)
# task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

# # サンプリングレートの設定 (1000サンプル/秒)
# task.timing.cfg_samp_clk_timing(1000)

# # タスクの開始
# task.start()

# # 10回データを取得
# for _ in range(10):
#   value = task.read()
#   print(f"電圧値: {value}V")
#   time.sleep(0.1)  # 0.1秒ごとに取得

# # タスクの終了
# task.stop()
# task.close()




import time
import datetime

n = 10
start_time = time.perf_counter()
print(start_time)
data = []
value = [0.0] * 16  # 16チャンネル分のデータを0.0で初期化


for k in range(n):
  now = datetime.datetime.now()
  step_time = time.perf_counter()
  value[0:0] = [now, step_time - start_time]
  print(value)
  data = data.append(value)

print(data)