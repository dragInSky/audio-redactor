def clear_history():
    with open('history/history.txt', 'w') as handle:
        handle.write('history of actions:\n')


def file_append(data: str):
    with open('history/history.txt', 'a') as handle:
        handle.write(data + '\n')


def get_text():
    with open('history/history.txt', 'r') as handle:
        return handle.read()
