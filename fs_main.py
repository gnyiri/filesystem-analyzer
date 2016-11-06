import sys
import getopt
import logging
from PyQt5.Qt import QApplication

from ui.fs_mainwindow import FS_MainWindow
from util.fs_logger import FS_Logger


def print_help():
    pass


if __name__ == '__main__':
    logger = FS_Logger.get_instance()
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

    logger.debug("Start application")
    APP = QApplication(sys.argv)
    ui = FS_MainWindow()
    ui.show()
    sys.exit(APP.exec_())