import pathlib

import os.path

SPEED = 1
VOLUME = 0

HOME = str(pathlib.Path.home())
TMP_EXPORT_PATH = os.path.join(str(pathlib.Path().resolve()) + '/resources/tmp_save.wav')
