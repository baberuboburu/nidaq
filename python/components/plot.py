import matplotlib.pyplot as plt
import pandas as pd
import os


class Plot:
  def __init__(self, username: str, filename: str):
    self.file_path = os.path.join(f'./img/{username}', filename)
    os.makedirs(os.path.dirname(self.file_path), exist_ok=True)


  def plot(self, df: pd.DataFrame, columns: list):
    # DataFrameの設定
    time_column = 'elapsed_time'

    # 電圧データを取得
    voltage_columns = columns[2:] 
    print(voltage_columns)

    plt.figure(figsize=(10, 6))

    for col in voltage_columns:
      plt.plot(df[time_column], df[col], label=col)
      plt.title(f'Voltage: {col} over Time')
      plt.xlabel('Time (s)')
      plt.ylabel('Voltage (V)')
      plt.legend()
      plt.grid(True)
      plt.savefig(self.file_path)
      plt.close()
    
    return