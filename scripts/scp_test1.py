# from htekTestTools.phones import Phone
#
# p1 = Phone('10.3.2.72', '3062')
# p1.dial('3036')
import os


def print_dir():
    print(os.getcwd())
    print(os.path.curdir)
    print(os.path.abspath('../..'))
