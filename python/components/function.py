import numpy as np


class Function():
  def __init__(self, n: int):
    '''
    入力波形の辞書クラス。
    n: データ点数
    '''
    self.n = n
  

  async def main(self, func: str, vol: float = None, amplitude: float = None, frequency: float = None, sampling_rate: float = None):
    if func == 'dc':
      return await self.dc(vol)

    elif func == 'sinx':
      return await self.sinx(amplitude, frequency, sampling_rate)
    
    elif func == 'cosx':
      return await self.cosx(amplitude, frequency, sampling_rate)
    
    elif func == 'triangle':
      return await self.triangle(amplitude, frequency, sampling_rate)
    
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


  async def triangle(self, amplitude: float, frequency: float, sampling_rate: float) -> list[float]:
    '''
    三角波
    amplitude: 振幅
    frequency: 周波数
    sampling_rate: サンプリング周波数
    '''
    t = np.linspace(0, self.n / sampling_rate, self.n, endpoint=False)
    output_vols = amplitude * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency)))
    return output_vols.tolist()


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

