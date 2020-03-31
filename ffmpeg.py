import os


def crop(input, start, end, output):
    command = 'ffmpeg -i {} -ss {} -to {} -c copy {}'.format(
        input, start, end, output)

    os.system(command)
    print(command)


def concat(input, output):
    command = 'ffmpeg -f concat -i {} -c copy {}'.format(input, output)

    os.system(command)
    print(command)
