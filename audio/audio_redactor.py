from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup
from history import history_handler


def get_cur_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AudioRedactor:
    def __init__(self):
        self.sound = AudioSegment.empty()

    def setSound(self, new_sound: AudioSegment) -> None:
        self.sound = new_sound

    def sound_from_file(self, file_path: str, fmt: str) -> None:
        if fmt == 'wav' or fmt == 'mp3':
            self.sound = AudioSegment.from_file(file_path, fmt)
            return

        history_handler.file_append(f'unknown file format: {fmt};\t[{get_cur_date()}]')
        self.sound = AudioSegment.empty()

    def start_cut(self, start_pos: float) -> None:
        if self.sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(self.sound):
            history_handler.file_append(f'incorrect data or cut position;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'file cut in {start_pos} secs from the start;\t[{get_cur_date()}]')

        start_pos *= 1000

        self.sound = self.sound[start_pos:len(self.sound)]

    def end_cut(self, end_pos: float) -> None:
        if self.sound == AudioSegment.empty() or end_pos <= 0 or end_pos * 1000 >= len(self.sound):
            history_handler.file_append(f'incorrect data or cut position;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'file cut in {end_pos} secs from the end;\t[{get_cur_date()}]')

        end_pos *= 1000

        self.sound = self.sound[:-end_pos]

    def start_end_cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(self.sound) \
                or end_pos <= 0 or end_pos * 1000 >= len(self.sound):
            history_handler.file_append(f'incorrect data or cut positions;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'file cut in {start_pos} secs from the start '
                                    f'and in {end_pos} secs from the end;\t[{get_cur_date()}]')

        start_pos *= 1000
        end_pos *= 1000

        self.sound = self.sound[start_pos:end_pos]

    def fragment_cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty() or start_pos <= 0 or start_pos * 1000 >= len(self.sound) \
                or end_pos <= 0 or end_pos * 1000 >= len(self.sound):
            history_handler.file_append(f'incorrect data or cut positions;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'fragment from {start_pos} to {end_pos} secs '
                                    f'was cut from the file;\t[{get_cur_date()}]')

        start_pos *= 1000
        end_pos *= 1000

        self.sound = self.sound[:start_pos] + self.sound[end_pos:]

    def append(self, sound2: AudioSegment) -> None:
        if self.sound == AudioSegment.empty() or sound2 == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'sound2 appended to the end of sound1;\t[{get_cur_date()}]')

        self.sound = self.sound + sound2

    def overlay(self, sound2: AudioSegment) -> None:
        if self.sound == AudioSegment.empty() or sound2 == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'overlay sounds;\t[{get_cur_date()}]')

        self.sound = self.sound.overlay(sound2)

    def reverse(self) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'sound reversed;\t[{get_cur_date()}]')

        self.sound = self.sound.reverse()

    def change_volume(self, value: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        if value >= 0:
            history_handler.file_append(f'sound volume was changed on +{value};\t[{get_cur_date()}]')
        else:
            history_handler.file_append(f'sound volume was changed on {value};\t[{get_cur_date()}]')

        self.sound += value

    def change_speed(self, speed_ratio: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'incorrect data;\t[{get_cur_date()}]')
            self.sound = AudioSegment.empty()
            return

        history_handler.file_append(f'sound speed changed in {speed_ratio};\t[{get_cur_date()}]')

        if speed_ratio >= 1:
            self.sound = speedup(self.sound, speed_ratio)
            return

        # speedup() в pydub умеет только ускорять аудио,
        # поэтому необходимо сделать дополнительные преобразования
        # Изменение частоты кадров. Отвечает за то, как много сэмплов в секунду играть
        sound_with_altered_frame_rate = self.sound._spawn(self.sound.raw_data, overrides={
            "frame_rate": int(self.sound.frame_rate * speed_ratio)
        })

        # Возвращение частоты кадров к стандартной
        self.sound = sound_with_altered_frame_rate.set_frame_rate(self.sound.frame_rate)

    def export(self, out_path: str, fmt: str) -> None:
        # обработка некорректного пути
        if fmt != 'wav' and fmt != 'mp3':
            history_handler.file_append(f'unknown format for export;\t[{get_cur_date()}]')

        history_handler.file_append(f'sound saved in {out_path} in {fmt} format;\t[{get_cur_date()}]')

        self.sound.export(out_path, fmt)
