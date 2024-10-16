import matplotlib.pyplot as plt
import pandas as pd
import os


class Plot:
  def __init__(self, username: str, filename: str):
    self.file_path = os.join(f'./img/{username}', filename)
    os.makedirs(os.path.dirname(self.file_path), exist_ok=True)


  def plot(self, data: list, columns: list):
    # DataFrameの設定
    df = pd.DataFrame(data, columns=columns)
    time_column = '経過時間'

    # 電圧データを取得
    voltage_columns = columns[2:]  

    plt.figure(figsize=(10, 6))

    for col in voltage_columns:
      plt.plot(df[time_column], df[col], label=col)
      plt.title('Voltage over Time')
      plt.xlabel('Time (s)')
      plt.ylabel('Voltage (V)')
      plt.legend()
      plt.grid(True)
      plt.savefig(self.file_path)
      plt.show()
    
    return