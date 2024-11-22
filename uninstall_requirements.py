import subprocess

with open("requirements.txt", "r") as file:
    packages = [line.split("==")[0].strip() for line in file if line.strip() and not line.startswith("#")]

for package in packages:
    subprocess.call(["pip", "uninstall", "-y", package])