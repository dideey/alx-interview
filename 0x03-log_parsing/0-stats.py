#!/usr/bin/python3
"""
this script reads stdin line by line and computes metrics

"""
import sys
import re
import signal


def format_check(data):
    """
    Checks if the data is in the correct format
    """
    pattern = re.compile(
        r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - "
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})\] "
        r'"GET \/projects\/260 HTTP\/1\.1" (\d{3}) (\d+)'
    )
    return bool(pattern.match(data))


def log_passing():
    """
    status code stats
    """
    status_code = {
        200: 0,
        301: 0,
        400: 0,
        401: 0,
        403: 0,
        404: 0,
        405: 0,
        500: 0
    }
    total_size = 0
    counter = 0

    def signal_handler(signum, frame):
        """
        handle SIGINT
        """
        print("File size: {}".format(total_size))
        for key in sorted(status_code.keys()):
            if status_code[key] != 0:
                print("{}: {}".format(key, status_code[key]))
        sys.exit(0)

    # Register the signal handler for SIGINT (CTRL + C)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        for line in sys.stdin:
            try:
                if not format_check(line):
                    continue
                counter += 1
                data = line.split()
                total_size += int(data[-1])

                status = int(data[-2])
                if status in status_code:
                    status_code[status] += 1
                if counter == 10:
                    print("File size: {}".format(total_size))
                    for key in sorted(status_code.keys()):
                        if status_code[key] != 0:
                            print("{}: {}".format(key, status_code[key]))
                    counter = 0

            except Exception as e:
                # If any other exception occurs, skip the line
                continue

    except KeyboardInterrupt:
        # If we get a keyboard interrupt, print the stats before exiting
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":
    log_passing()