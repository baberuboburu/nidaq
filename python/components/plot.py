import matplotlib.pyplot as plt
import pandas as pd
import os


class Plot:
  def __init__(self, username: str):
    self.file_dir = f'./img/{username}'
    os.makedirs(self.file_dir, exist_ok=True)


  def plot_voltage_vs_time(self, df: pd.DataFrame, columns: list):
    # 時間を基準に電圧をプロット
    time_column = 'elapsed_time'
    voltage_columns = columns[2:] 

    plt.figure(figsize=(10, 6))
    for col in voltage_columns:
      plt.plot(df[time_column], df[col], label=col)
      plt.title('Voltage vs Time')
      plt.xlabel('Time (s)')
      plt.ylabel('Voltage (V)')
      plt.legend()
      plt.grid(True)
      plt.savefig(os.path.join(self.file_dir, f'VT_{col}.png'))
      plt.close()


  def plot_iv_curve(self, df: pd.DataFrame):
    # 出力電圧と入力電圧 (I-V 特性)をプロット
    print(df.head(3))
    plt.figure(figsize=(10, 6))

    for col in df.columns:
      print(col)
      if col.startswith('voltage_ai'):
        plt.plot(df['voltage_ao0'], df[col], '-', label=f"IV_{col}")
        plt.title('I-V Characteristics')
        plt.xlabel('Input Voltage (V)')
        plt.ylabel('Output Voltage (V)')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.file_dir, f'IV_{col}.png'))
        plt.close()


  def plot_dc(self, df: pd.DataFrame):
    # 出力電圧と入力電圧 (I-V 特性)をプロット
    plt.figure(figsize=(10, 6))

    for col in df.columns:
      print(col)
      if col.startswith('voltage_ai'):
        plt.plot(df['elapsed_time'], df[col], '-', label=f"IT_{col}")
        plt.title('I-V Characteristics')
        plt.xlabel('Input Voltage (V)')
        plt.ylabel('Output Voltage (V)')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.file_dir, f'DC_IV{col}.png'))
        plt.close()