def clear_history():
    with open('history.txt', 'wb'):
        pass


def file_append(data: str):
    with open('history.txt', "a") as handle:
        handle.write(data + '\n')
