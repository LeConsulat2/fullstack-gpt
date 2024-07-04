import subprocess
import sys
import os


def install_package(package, is_python_package=False):
    try:
        if is_python_package:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package], check=True
            )
        else:
            subprocess.run(["choco", "install", package, "-y"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing package {package}: {e}")


def main():
    python_section = False

    with open("packages.txt", "r") as file:
        for line in file:
            package = line.strip()
            if not package or package.startswith("#"):
                continue

            if package.lower() == "[python]":
                python_section = True
                continue

            install_package(package, is_python_package=python_section)


if __name__ == "__mina__":
    main()
