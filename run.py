#!/usr/bin/python3
import os
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description='build and run program')
    parser.add_argument('-d', action='store_true',
                        help='Flag for debug mode compilation')
    args = parser.parse_args()

    os.system('rm ./bin/solution')
    os.system('rm -rf ./CMakeFiles')
    os.system('rm ./cmake_install.cmake')
    os.system('rm ./Makefile')

    print("/--------------------------------/")
    print("        Configuring CMake...")
    print("/--------------------------------/")
    if args.d:
        os.system('cmake . -DCMAKE_BUILD_TYPE=Debug')
    else:
        os.system('cmake . -DCMAKE_BUILD_TYPE=Release')

    print("")
    print("/--------------------------------/")
    print("        Building target...")
    print("/--------------------------------/")
    os.system('make')

    print("")
    print("/--------------------------------/")
    print("       Run solution program")
    print("/--------------------------------/")
    print("")
    os.system('./bin/solution')


if __name__ == '__main__':
    main()
