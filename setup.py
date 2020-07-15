from cx_Freeze import setup, Executable

packages = ['cv2','numpy','ctypes','os','time']


setup(name = 'detector_LEDs',
      version = '1.0.0',
      description = 'LED detector app',
      options = {'build_exe': {'packages': packages}},
      executables = [Executable("detector_LEDs.py")])