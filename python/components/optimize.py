import pandas as pd
import numpy as np
from typing import List


class Optimize():
  def __init__(self):
    '''
    解析指標
     - 最大電流値
     - 非線形性
     - キャパシタ容量 + メモリ特性
    '''
    pass


  async def main(self, df: pd.DataFrame, optimize: str):
    # arranged_df = await self.arrange(df)
    optimized_ai = await self.routing(df, optimize)

    return optimized_ai
  

  async def arrange(self, df: pd.DataFrame ) -> pd.DataFrame:
    column_names = ['timestamp', 'elapsed_time'] + [f'voltage_ai{i}' for i in range(len(df[0]) - 2)]
    df = pd.DataFrame(df, columns=column_names)
    scaled_df = self.scale(df)

    return scaled_df
  

  async def scale(self, df: pd.DataFrame) -> pd.DataFrame:
    # 'voltage_ai' で始まるカラムのみを対象
    for col in df.columns:
      if col.startswith('voltage_ai'):
        max_value = df[col].max()
        if max_value != 0:  # ゼロの場合を回避
          # 最大値のオーダーを取得
          order_of_magnitude = int(np.floor(np.log10(abs(max_value))))
          # 全てのデータが10^0オーダーになるようにスケールを調整
          scaling_factor = 10 ** -order_of_magnitude
          df[col] = df[col] * scaling_factor
          print(f"{col} の最大値: {max_value}, オーダー: 10^{order_of_magnitude}")
    
    return df
  

  async def routing(self, df: pd.DataFrame, optimize: str):
    if optimize == 'current':
      return await self.current(df)
    elif optimize == 'capacitance':
      return await self.capacitance(df)
    elif optimize == 'nonlinearity':
      return await self.nonlinearity(df, small_vol=0.2, large_vol=0.8)
    elif optimize == 'histeresis':
      return await self.histeresis(df)
    else:
      raise ValueError(f'optimize変数が正しく設定されていません。\n指定されたoptimize変数: {optimize}')
  

  async def current(self):
    return
  

  async def capacitance(self):
    return
  

  async def nonlinearity(self, df, small_vol: float, large_vol: float) -> List[str]:
    # 数値カラムのみを抽出して微分を計算
    numeric_df = df.select_dtypes(include=[float, int]).copy()
    derivative_df = numeric_df.diff().fillna(0)

    # データの上から1/4に含まれる範囲を選択
    quarter_length = len(numeric_df) // 4
    subset_df = numeric_df.iloc[:quarter_length]
    derivative_subset_df = derivative_df.iloc[:quarter_length]

    # 'voltage_ai' で始まるカラムのみを対象に微分係数を取得
    closest_small_derivatives = {}
    closest_large_derivatives = {}
    
    for col in derivative_subset_df.columns:
      if col.startswith('voltage_ai'):  # 'voltage_ai' で始まるカラムのみを対象
        print(f'------------ {col} ------------')
        # small_volに最も近い点（上から1/4の範囲で）
        print(f'--- {small_vol}V ---')
        closest_small_idx = (subset_df['voltage_ao0'] - small_vol).abs().idxmin()
        closest_small_derivatives[col] = derivative_subset_df.loc[closest_small_idx, col]
        print(f"微分係数: {closest_small_derivatives[col]}")
        print(f"(voltage_ao0, {col}): ({subset_df.loc[closest_small_idx, 'voltage_ao0']}, {subset_df.loc[closest_small_idx, col]})")
        
        # large_volに最も近い点（上から1/4の範囲で）
        print(f'--- {large_vol}V ---')
        closest_large_idx = (subset_df['voltage_ao0'] - large_vol).abs().idxmin()
        closest_large_derivatives[col] = derivative_subset_df.loc[closest_large_idx, col]
        print(f"微分係数: {closest_large_derivatives[col]}")
        print(f"(voltage_ao0, {col}): ({subset_df.loc[closest_large_idx, 'voltage_ao0']}, {subset_df.loc[closest_large_idx, col]})")

    print('-------------------------------------')
    # 微分係数の差が大きい順にカラム名をソート
    diff_list = [
      (col, abs(closest_large_derivatives[col] - closest_small_derivatives[col]))
      for col in closest_small_derivatives.keys()
    ]
    diff_list.sort(key=lambda x: x[1], reverse=True)
    
    # 差が大きい順にカラム名をリストに追加して返す
    sorted_columns = [col for col, _ in diff_list]
    
    print(f"差が大きい順のカラムリスト: {sorted_columns}")
    return sorted_columns


  
  async def histeresis(self):
    return