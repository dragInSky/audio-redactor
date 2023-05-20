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
        self.sound2 = AudioSegment.empty()

    def set_sound(self, new_sound_path: str, new_sound_format: str) -> None:
        self.sound = self.sound_from_file(new_sound_path, new_sound_format)

    def set_sound2(self, new_sound_path: str, new_sound_format: str) -> None:
        self.sound2 = self.sound_from_file(new_sound_path, new_sound_format)

    @staticmethod
    def sound_from_file(file_path: str, fmt: str) -> AudioSegment:
        history_handler.import_info(file_path, fmt)
        return AudioSegment.from_file(file_path, fmt)

    def reverse(self) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        history_handler.reverse_info()
        self.sound = self.sound.reverse()

    def change_speed(self, speed_ratio: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        self.speed_ratio = speed_ratio
        history_handler.speed_info(speed_ratio)

    def refresh_speed(self):
        self.speed_ratio = base_values.SPEED
        history_handler.speed_info(base_values.SPEED)

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
            history_handler.error_empty_source()
            return

        history_handler.volume_info(value)
        self.volume += value
        self.sound += value

    def silent_refresh_volume(self):
        history_handler.volume_info(self.volume)
        self.volume = 0
        self.sound -= self.volume

    def refresh_volume(self) -> None:
        history_handler.volume_info(self.volume)
        self.change_volume(-self.volume)
        history_handler.volume_info(-self.volume)

    def cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        if start_pos < 0 or start_pos * 1000 > len(self.sound) \
                or end_pos < 0 or end_pos * 1000 > len(self.sound):
            history_handler.error_incorrect_data(start_pos, end_pos)
            return

        start_pos *= 1000
        end_pos *= 1000

        history_handler.cut_info(start_pos, end_pos)

        self.sound = self.sound[start_pos:end_pos]

    def fragment_cut(self, start_pos: float, end_pos: float) -> None:
        if self.sound == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        if start_pos < 0 or start_pos * 1000 > len(self.sound) \
                or end_pos < 0 or end_pos * 1000 > len(self.sound):
            history_handler.error_incorrect_data(start_pos, end_pos)
            return

        start_pos *= 1000
        end_pos *= 1000

        history_handler.fragment_info(start_pos, end_pos)

        self.sound = self.sound[:start_pos] + self.sound[end_pos:]

    def append(self) -> None:
        if self.sound == AudioSegment.empty() or self.sound2 == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        history_handler.append_info()
        self.sound = self.sound + self.sound2

    def overlay(self) -> None:
        if self.sound == AudioSegment.empty() or self.sound2 == AudioSegment.empty():
            history_handler.error_empty_source()
            return

        history_handler.overlay_info()
        self.sound = self.sound.overlay(self.sound2)

    def audio_export(self, out_path: str, fmt: str) -> None:
        if fmt != 'wav' and fmt != 'mp3':
            history_handler.error_unknown_format(fmt)

        history_handler.export_info(out_path, fmt)
        self._change_speed().export(out_path, fmt)
