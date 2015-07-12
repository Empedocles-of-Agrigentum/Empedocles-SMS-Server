import sys
import os

import daemon

if __name__ == "__main__":
    D = daemon.SMSDaemon("/var/run/sms_daemon.pid")
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            D.start()
        elif sys.argv[1] == "stop":
            D.stop()
        elif sys.argv[1] == "restart":
            D.restart()
        else:
            print "Unrecognized command line argument!" + sys.argv[1]
    else:
        print "No action specified, use start, stop or restart"
