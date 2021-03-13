import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Script for project setup')
    parser.add_argument('--toolchain', action='store_true',
                        help='Flag for installing essential C++ toolchains: \
                            clang, \
                            gcc, \
                            clang-tools \
                            clang-tidy \
                            lldb \
                            lld \
                            libc++ \
                            libomp')
    args = parser.parse_args()

    if args.toolchain:
        os.system('chmod +x ./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('chmod +x ./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        os.system('./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('./scripts/cpp_tool_chains/install_llvm_toolchain.sh')

    print("Setup complete!")


if __name__ == '__main__':
    main()
