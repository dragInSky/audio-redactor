from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup
from history import history_handler
from audio import base_values


def get_cur_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AudioRedactor:
    def __init__(self):
        self.volume = base_values.VOLUME
        self.speed_ratio = base_values.SPEED
        self.sound = AudioSegment.empty()

    def set_sound(self, new_sound) -> None:
        self.sound = new_sound

    def sound_from_file(self, file_path: str, fmt: str) -> None:
        if fmt == 'wav' or fmt == 'mp3':
            history_handler.file_append(f'(import) from {file_path} in {fmt};\t[{get_cur_date()}]')
            self.sound = AudioSegment.from_file(file_path, fmt)
            return

        history_handler.file_append(f'[error](import) unknown file format: {fmt};\t[{get_cur_date()}]')

    def reverse(self) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'[error](reverse) incorrect data;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(reverse) success;\t[{get_cur_date()}]')

        self.sound = self.sound.reverse()

    def change_speed(self, speed_ratio: float) -> None:
        self.speed_ratio = speed_ratio
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'[error](speed) incorrect data;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(speed) {speed_ratio}x;\t[{get_cur_date()}]')

    def refresh_speed(self):
        self.speed_ratio = base_values.SPEED

    def _change_speed(self) -> AudioSegment:
        if self.speed_ratio > 1:
            return speedup(self.sound, self.speed_ratio)

        # speedup() в pydub умеет только ускорять аудио,
        # поэтому необходимо сделать дополнительные преобразования
        # Изменение частоты кадров. Отвечает за то, как много сэмплов в секунду играть
        sound_with_altered_frame_rate = self.sound._spawn(self.sound.raw_data, overrides={
            "frame_rate": int(self.sound.frame_rate * self.speed_ratio)
        })

        # Возвращение частоты кадров к стандартной
        return sound_with_altered_frame_rate.set_frame_rate(self.sound.frame_rate)

    def change_volume(self, value: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.file_append(f'[error](volume) incorrect data;\t[{get_cur_date()}]')
            return

        if value >= 0:
            history_handler.file_append(f'(volume) +{value}db;\t[{get_cur_date()}]')
        else:
            history_handler.file_append(f'(volume) {value}db;\t[{get_cur_date()}]')

        self.volume += value
        self.sound += value

    def refresh_volume(self) -> None:
        self.change_volume(-self.volume)

    def cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty() or start_pos < 0 or start_pos * 1000 > len(self.sound) \
                or end_pos < 0 or end_pos * 1000 > len(self.sound):
            history_handler.file_append(f'[error](cut) incorrect data or cut positions;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(cut) from {start_pos} to {end_pos};\t[{get_cur_date()}]')

        start_pos *= 1000
        end_pos *= 1000

        self.sound = self.sound[start_pos:end_pos]

    def fragment_cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty() or start_pos < 0 or start_pos * 1000 > len(self.sound) \
                or end_pos < 0 or end_pos * 1000 > len(self.sound):
            history_handler.file_append(f'[error](fragment cut) incorrect data or cut positions;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(fragment cut) fragment from {start_pos} to {end_pos};\t[{get_cur_date()}]')

        start_pos *= 1000
        end_pos *= 1000

        self.sound = self.sound[:start_pos] + self.sound[end_pos:]

    def append(self, sound2: AudioSegment) -> None:
        if self.sound == AudioSegment.empty() or sound2 == AudioSegment.empty():
            history_handler.file_append(f'[error](append) incorrect data;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(append) success;\t[{get_cur_date()}]')

        self.sound = self.sound + sound2

    def overlay(self, sound2: AudioSegment) -> None:
        if self.sound == AudioSegment.empty() or sound2 == AudioSegment.empty():
            history_handler.file_append(f'[error](overlay) incorrect data;\t[{get_cur_date()}]')
            return

        history_handler.file_append(f'(overlay) success;\t[{get_cur_date()}]')

        self.sound = self.sound.overlay(sound2)

    def audio_export(self, out_path: str, fmt: str) -> None:
        # обработка некорректного пути
        if fmt != 'wav' and fmt != 'mp3':
            history_handler.file_append(f'[error](export) unknown format: {fmt};\t[{get_cur_date()}]')

        history_handler.file_append(f'(export) export to {out_path} in {fmt};\t[{get_cur_date()}]')

        self._change_speed().export(out_path, fmt)
