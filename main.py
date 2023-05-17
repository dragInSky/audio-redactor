from audio_processing import audio_operations


def main():
    sound1 = audio_operations.sound_from_file("sample_data/s1.wav", "wav")
    # sound2 = AudioSegment.from_file("sample_data/s2.wav", format="wav")

    res_sound = audio_operations.start_cut(sound1, 1)
    audio_operations.export(res_sound, "output/startCut.wav", "wav")


if __name__ == '__main__':
    main()
