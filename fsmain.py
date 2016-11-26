import sys
import getopt
import logging
from PyQt5.Qt import QApplication

from ui.fsmainwindow import FSMainWindow
from util.fslogger import FSLogger


def print_help():
    print("help: help")


if __name__ == '__main__':
    logger = FSLogger.get_instance()
    logger.setLevel(logging.DEBUG)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
        # parse command line arguments
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                print_help()
                sys.exit()
            else:
                print_help()
                sys.exit()
    except getopt.GetoptError:
        print_help()

    logger.info("Start application")
    APP = QApplication(sys.argv)
    ui = FSMainWindow()
    ui.show()
    sys.exit(APP.exec_())
