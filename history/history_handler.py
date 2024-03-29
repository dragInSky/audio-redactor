from datetime import datetime

import os.path

HISTORY_PATH = os.path.join('history/history.txt')


def get_cur_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ser_id():
    return "id: " + datetime.now().strftime("%f") + " > "


def clear_history():
    with open(HISTORY_PATH, 'w') as handle:
        handle.write('history of actions:\n')


def file_append(data: str):
    with open(HISTORY_PATH, 'a') as handle:
        handle.write(data + '\n')


def get_text():
    with open(HISTORY_PATH, 'r') as handle:
        return handle.read()


def import_info(file_path: str, fmt: str):
    file_append(f'{ser_id()}(import) from {file_path} in {fmt}\t[{get_cur_date()}]')


def error_empty_source():
    file_append(f'{ser_id()}empty source sound\t[{get_cur_date()}]')


def error_incorrect_data(start_pos: float, end_pos: float):
    file_append(f'{ser_id()}incorrect cur positions: {start_pos} - {end_pos}\t[{get_cur_date()}]')


def error_unknown_format(fmt: str):
    file_append(f'{ser_id()}unknown format: {fmt}\t[{get_cur_date()}]')


def reverse_info():
    file_append(f'{ser_id()}(reverse) success\t[{get_cur_date()}]')


def speed_info(speed_ratio: float):
    file_append(f'{ser_id()}(speed) {speed_ratio}x\t[{get_cur_date()}]')


def volume_info(value: float):
    if value >= 0:
        file_append(f'{ser_id()}(volume) +{value}db\t[{get_cur_date()}]')
    else:
        file_append(f'{ser_id()}(volume) {value}db\t[{get_cur_date()}]')


def cut_info(start_pos: float, end_pos: float):
    file_append(f'{ser_id()}(cut) from {start_pos} to {end_pos}\t[{get_cur_date()}]')


def fragment_info(start_pos: float, end_pos: float):
    file_append(f'{ser_id()}(fragment cut) fragment from {start_pos} to {end_pos}\t[{get_cur_date()}]')


def append_info():
    file_append(f'{ser_id()}(append) success\t[{get_cur_date()}]')


def overlay_info():
    file_append(f'{ser_id()}(overlay) success\t[{get_cur_date()}]')


def export_info(out_path: str, fmt: str):
    file_append(f'{ser_id()}(export) export to {out_path} in {fmt}\t[{get_cur_date()}]')


def info_text(text: str):
    file_append(f'{ser_id()}{text}\t[{get_cur_date()}]')
