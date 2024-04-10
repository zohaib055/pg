try:
    import time
    import sys
    import os
    print(sys.argv[1])
    directory = os.getcwd()

    print(directory)
    for x in range(0,5):
        print(x)
        sys.stdout.flush()
        time.sleep(5)
except:
    exit(0)