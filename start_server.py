from server_control import *
import sys

os.system('cls || clear')
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(is_cli=False, arg=sys.argv[1:])
    else:
        main(is_cli=True)
