from PythonChessMain import PythonChessMain

from optparse import OptionParser
import time, sys, random

class Policy:

    def __init__(self):
        return


def run_game():
    parser = OptionParser()
    parser.add_option("-d", dest="debug",
                      action="store_true", default=False, help="Enable debug mode (different starting board configuration)")
    parser.add_option("-t", dest="text",
                      action="store_true", default=True, help="Use text-based GUI")
    parser.add_option("-o", dest="old",
                      action="store_true", default=False, help="Use old graphics in pygame GUI")
    parser.add_option("-p", dest="pauseSeconds", metavar="SECONDS",
                      action="store", default=0, help="Sets time to pause between moves in AI vs. AI games (default = 0)")


    (options,args) = parser.parse_args()
    game = PythonChessMain(options)
    game.sim_setup(options)
    game.MainLoop()
    print(game.player[game.winnerIndex].GetColor())
    return game.turnCount

def main():
    count = 0
    for i in range(100):
        count += run_game()
    count /= 100.0
    print(count)
    return

if __name__ == "__main__":
    main()
