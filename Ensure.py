# import subprocess
# import sys
# import os


# def install_package(package, is_python_package=False):
#     try:
#         if is_python_package:
#             print(f"Installing Python package: {package}")
#             subprocess.run(
#                 [sys.executable, "-m", "pip", "install", package], check=True
#             )
#         else:
#             print(f"Installing system package: {package}")
#             subprocess.run(["choco", "install", package, "-y"], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error installing package {package}: {e}")
#         raise


# def main():
#     python_section = False

#     if not os.path.exists("packages.txt"):
#         print("packages.txt not found.")
#         return

#     with open("packages.txt", "r") as file:
#         for line in file:
#             package = line.strip()
#             if not package or package.startswith("#"):
#                 continue

#             if package.lower() == "[python]":
#                 python_section = True
#                 continue

#             try:
#                 install_package(package, is_python_package=python_section)
#             except Exception as e:
#                 print(f"Failed to install {package}. Error: {e}")
#                 sys.exit(1)


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         sys.exit(1)
