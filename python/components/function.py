import numpy as np
from scipy import signal


class Function():
  def __init__(self, n: int):
    '''
    入力波形の辞書クラス。
    n: データ点数
    '''
    self.n = n
  

  async def main(self, func: str, vol: float = None, amplitude: float = None, n_cycle: int = 1, frequency: float = None, sampling_rate: float = None):
    if func == 'dc':
      return await self.dc(vol)

    elif func == 'sinx':
      return await self.sinx(amplitude, frequency, sampling_rate)
    
    elif func == 'cosx':
      return await self.cosx(amplitude, frequency, sampling_rate)
    
    elif func == 'triangle':
      return await self.triangle(amplitude, n_cycle)
    
    elif func == 'sawtooth':
      return await self.sawtooth(amplitude, frequency, sampling_rate)
    
    else:
      raise ValueError(f'func is invalid. Your select is {func}.\nYou should select in ["dc", "sinx", "cosx", "triagle", "sawtooth"].')


  async def dc(self, vol: float) -> list[float]:
    '''
    DC（直流）波形
    vol: 電圧値
    '''
    output_vols = [vol] * self.n
    return output_vols


  async def sinx(self, amplitude: float, frequency: float, sampling_rate: float) -> list[float]:
    '''
    正弦波
    amplitude: 振幅
    frequency: 周波数
    sampling_rate: サンプリング周波数
    '''
    t = np.linspace(0, self.n / sampling_rate, self.n, endpoint=False)
    output_vols = amplitude * np.sin(2 * np.pi * frequency * t)
    return output_vols.tolist()


  async def cosx(self, amplitude: float, frequency: float, sampling_rate: float) -> list[float]:
    '''
    余弦波
    amplitude: 振幅
    frequency: 周波数
    sampling_rate: サンプリング周波数
    '''
    t = np.linspace(0, self.n / sampling_rate, self.n, endpoint=False)
    output_vols = amplitude * np.cos(2 * np.pi * frequency * t)
    return output_vols.tolist()


  async def triangle(self, amplitude: float, n_cycle: int) -> list[float]:
    '''
    三角波
    amplitude: 振幅
    n_cycle: 周期の回数
    '''
    # 各セクションの長さを計算
    period = self.n // n_cycle
    quarter = period // 4
    half = period // 2
  
    # 三角波の各セクションを作成
    rise = np.linspace(0, amplitude, quarter, endpoint=False)        # 0 → amplitude
    fall = np.linspace(amplitude, -amplitude, half, endpoint=False)  # amplitude → -amplitude
    rise_back = np.linspace(-amplitude, 0, quarter, endpoint=False)  # -amplitude → 0
  
    # セクションを結合して1周期の三角波を作成
    triangle_wave = np.concatenate([rise, fall, rise_back])
  
    # 周期の回数に応じてデータを複製
    triangle_wave = np.tile(triangle_wave, n_cycle)
  
    # 結果を表示してリストとして返す
    print(triangle_wave)
    return triangle_wave.tolist()



  async def sawtooth(self, amplitude: float, frequency: float, sampling_rate: float) -> list[float]:
    '''
    方形波（ノコギリ波）
    amplitude: 振幅
    frequency: 周波数
    sampling_rate: サンプリング周波数
    '''
    t = np.linspace(0, self.n / sampling_rate, self.n, endpoint=False)
    output_vols = amplitude * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
    return output_vols.tolist()

