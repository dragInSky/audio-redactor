from pydub import AudioSegment

import audio_operations


def main():
    sound1 = AudioSegment.from_file("sample_data/s1.wav", format="wav")
    # sound2 = AudioSegment.from_file("sample_data/s2.wav", format="wav")

    sound = audio_operations.change_speed(sound1, 0.5)
    audio_operations.export(sound, "output/speedup.wav", "wav")


if __name__ == '__main__':
    main()
