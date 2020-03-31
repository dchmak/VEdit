import os


def crop(input, start, end, output):
    command = 'ffmpeg -loglevel error -i {} -ss {} -to {} -c copy {}'.format(
        input, start, end, output)

    print(command)
    return os.system(command)


def concat(input, output):
    command = 'ffmpeg -loglevel error -f concat -i {} -c copy {}'.format(input, output)

    print(command)
    return os.system(command)
