
import os

def get_gpu_info_windows():
    print(os.system('wmic path win32_videocontroller get caption'))
    # Füge hier weitere relevante Informationen hinzu, die du benötigst

get_gpu_info_windows()
