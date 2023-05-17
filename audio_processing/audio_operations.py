from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup

from operations_history import history_handler


def get_cur_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sound_from_file(file_path: str, fmt: str) -> AudioSegment:
    return AudioSegment.from_file(file_path, fmt)


def start_cut(sound: AudioSegment, start_pos: int) -> AudioSegment:
    history_handler.file_append(f'file cut from {start_pos} sec;\t[{get_cur_date()}]')

    start_pos *= 1000

    return sound[start_pos:len(sound)]


def end_cut(sound: AudioSegment, end_pos: int) -> AudioSegment:
    history_handler.file_append(f'file cut 0 - {end_pos} sec;\t[{get_cur_date()}]')

    end_pos *= 1000

    return sound[:-end_pos]


def cut(sound: AudioSegment, start_pos: int, end_pos: int) -> AudioSegment:
    history_handler.file_append(f'file cut from {start_pos} to {end_pos} sec;\t[{get_cur_date()}]')

    start_pos *= 1000
    end_pos *= 1000

    return sound[start_pos:end_pos]


def append(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
    history_handler.file_append(f'sound2 appended to the end of sound1;\t[{get_cur_date()}]')

    return sound1 + sound2


def overlay(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
    history_handler.file_append(f'overlay sound2 on sound1;\t[{get_cur_date()}]')

    return sound1.overlay(sound2)


def reverse(sound: AudioSegment) -> AudioSegment:
    history_handler.file_append(f'sound reversed;\t[{get_cur_date()}]')

    return sound.reverse()


def change_speed(sound: AudioSegment, speed_ratio: float) -> AudioSegment:
    history_handler.file_append(f'sound speed changed in {speed_ratio};\t[{get_cur_date()}]')

    if speed_ratio >= 1:
        return speedup(sound, speed_ratio)

    # speedup() в pydub умеет только ускорять аудио,
    # поэтому необходимо сделать дополнительные преобразования
    # Изменение частоты кадров. Отвечает за то, как много сэмплов в секунду играть
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed_ratio)
    })

    # Возвращение частоты кадров к стандартной
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def export(sound: AudioSegment, out_path: str, fmt: str) -> None:
    history_handler.file_append(f'sound saved in {out_path} in {fmt} format;\t[{get_cur_date()}]')

    sound.export(out_path, fmt)
