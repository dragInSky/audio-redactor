from pydub import AudioSegment
from pydub.effects import speedup


def start_cut(sound: AudioSegment, start_pos: int) -> AudioSegment:
    start_pos *= 1000

    return sound[start_pos:len(sound)]


def end_cut(sound: AudioSegment, end_pos: int) -> AudioSegment:
    end_pos *= 1000

    return sound[:-end_pos]


def cut(sound: AudioSegment, start_pos: int, end_pos: int) -> AudioSegment:
    start_pos *= 1000
    end_pos *= 1000

    return sound[start_pos:end_pos]


def append(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
    return sound1 + sound2


def overlay(sound1: AudioSegment, sound2: AudioSegment) -> AudioSegment:
    return sound1.overlay(sound2)


def reverse(sound: AudioSegment) -> AudioSegment:
    return sound.reverse()


def change_speed(sound: AudioSegment, speed_ratio: float) -> AudioSegment:
    if speed_ratio >= 1:
        return speedup(sound, speed_ratio)

    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed_ratio)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def export(sound: AudioSegment, out_path: str, fmt: str) -> None:
    sound.export(out_path, fmt)
