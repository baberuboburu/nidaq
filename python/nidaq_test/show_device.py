import nidaqmx
from nidaqmx.system import System


# システムに接続されているデバイスを取得
system = System.local()

# 接続されているすべてのデバイス名を表示
print("Devices connected:")
for device in system.devices:
    print(f"Device Name: {device.name}")

    # そのデバイスのアナログ入力チャネル（AI）を表示
    print("Analog Input Channels:")
    for ai_chan in device.ai_physical_chans:
        print(f"  {ai_chan.name}")

    # そのデバイスのアナログ出力チャネル（AO）を表示
    print("Analog Output Channels:")
    for ao_chan in device.ao_physical_chans:
        print(f"  {ao_chan.name}")