from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup

from operations_history import history_handler


def get_cur_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sound_from_file(file_path: str, fmt: str) -> AudioSegment:
    if fmt == 'wav' or fmt == 'mp3':
        return AudioSegment.from_file(file_path, fmt)

    history_handler.file_append(f'unknown file format: {fmt};\t[{get_cur_date()}]')
    return AudioSegment.empty()


def start_cut(sound: AudioSegment, start_pos: float) -> AudioSegment:
    if sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(sound):
        history_handler.file_append(f'incorrect data or cut position;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'file cut in {start_pos} secs from the start;\t[{get_cur_date()}]')

    start_pos *= 1000

    return sound[start_pos:len(sound)]


def end_cut(sound: AudioSegment, end_pos: float) -> AudioSegment:
    if sound == AudioSegment.empty() or end_pos <= 0 or end_pos * 1000 >= len(sound):
        history_handler.file_append(f'incorrect data or cut position;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'file cut in {end_pos} secs from the end;\t[{get_cur_date()}]')

    end_pos *= 1000

    return sound[:-end_pos]


def start_end_cut(sound: AudioSegment, start_pos: float, end_pos: float) -> AudioSegment:
    if sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(sound) \
            or end_pos <= 0 or end_pos * 1000 >= len(sound):
        history_handler.file_append(f'incorrect data or cut positions;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'file cut in {start_pos} secs from the start '
                                f'and in {end_pos} secs from the end;\t[{get_cur_date()}]')

    start_pos *= 1000
    end_pos *= 1000

    return sound[start_pos:end_pos]


def fragment_cut(sound: AudioSegment, start_pos: float, end_pos: float) -> AudioSegment:
    if sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(sound) \
            or end_pos <= 0 or end_pos * 1000 >= len(sound):
        history_handler.file_append(f'incorrect data or cut positions;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'fragment from {start_pos} to {end_pos} secs '
                                f'was cut from the file;\t[{get_cur_date()}]')

    start_pos *= 1000
    end_pos *= 1000

    return sound[:start_pos] + sound[end_pos:]


def append(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
    if sound1 == AudioSegment.empty() or sound2 == AudioSegment.empty():
        history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'sound2 appended to the end of sound1;\t[{get_cur_date()}]')

    return sound1 + sound2


def overlay(*sound_args: AudioSegment) -> AudioSegment:
    for sound in sound_args:
        if sound == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            return AudioSegment.empty()

    history_handler.file_append(f'overlay sounds;\t[{get_cur_date()}]')

    res_sound = AudioSegment.empty()
    for sound in sound_args:
        if res_sound == AudioSegment.empty():
            res_sound = sound
        else:
            res_sound = res_sound.overlay(sound)
    return res_sound


def reverse(sound: AudioSegment) -> AudioSegment:
    if sound == AudioSegment.empty():
        history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    history_handler.file_append(f'sound reversed;\t[{get_cur_date()}]')

    return sound.reverse()


def change_volume(sound: AudioSegment, value: float) -> AudioSegment:
    if value >= 20:
        value = 20
        history_handler.file_append(f'max db to add: +20;\t[{get_cur_date()}]')

    if sound == AudioSegment.empty():
        history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
        return AudioSegment.empty()

    if value >= 0:
        history_handler.file_append(f'sound volume was changed on +{value};\t[{get_cur_date()}]')
    else:
        history_handler.file_append(f'sound volume was changed on {value};\t[{get_cur_date()}]')

    return sound + value


def change_speed(sound: AudioSegment, speed_ratio: float) -> AudioSegment:
    if speed_ratio >= 10:
        speed_ratio = 10
        history_handler.file_append(f'audio speed limits: -10x to 10x;\t[{get_cur_date()}]')
    if speed_ratio <= -10:
        speed_ratio = -10
        history_handler.file_append(f'audio speed limits: -10x to 10x;\t[{get_cur_date()}]')

    if sound == AudioSegment.empty():
        history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
        return AudioSegment.empty()

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
    # обработка некорректного пути
    if fmt != 'wav' and fmt != 'mp3':
        history_handler.file_append(f'unknown format for export;\t[{get_cur_date()}]')

    history_handler.file_append(f'sound saved in {out_path} in {fmt} format;\t[{get_cur_date()}]')

    sound.export(out_path, fmt)
