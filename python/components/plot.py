import matplotlib.pyplot as plt
import pandas as pd
import os


class Plot:
  def __init__(self, username: str, filename: str):
    self.file_path = os.path.join(f'./img/{username}', filename)
    os.makedirs(os.path.dirname(self.file_path), exist_ok=True)


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
    plt.savefig(self.file_path.replace('.png', '_voltage_vs_time.png'))
    plt.close()


  def plot_iv_curve(self, df: pd.DataFrame):
    # 出力電圧と入力電圧 (I-V 特性)をプロット
    plt.figure(figsize=(10, 6))

    for col in df.columns:
      if col.startswith('voltage_ao'):
        plt.plot(df['voltage_ai0'], df[col], '-', label=f"I-V Curve for {col}")
    
    plt.title('I-V Characteristics')
    plt.xlabel('Input Voltage (V)')
    plt.ylabel('Output Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.savefig(self.file_path.replace('.png', '_iv_curve.png'))
    plt.close()