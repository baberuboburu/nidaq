import pandas as pd
import matplotlib.pyplot as plt

# サンプルデータを読み込む
df = pd.read_csv('sample.csv')

# プロット
plt.figure(figsize=(10, 6))

# 各入力カラムに対してプロット
for col in ['voltage_ai0', 'voltage_ai1', 'voltage_ai2']:
    plt.plot(df['output'], df[col], label=col)

# プロットの詳細設定
plt.xlabel('Output')
plt.ylabel('Input (voltage)')
plt.title('Input vs. Output')
plt.legend()
plt.grid(True)
plt.show()
