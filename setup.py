from setuptools import setup, find_packages

setup(
    name="smartos",
    version="1.0.0",
    packages=find_packages(),
    install_requires=open("smartos_requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "smartos=smartos_main:main"
        ]
    },
    author="myOnsite Healthcare LLC",
    description="SmartOS - Voice/Chat-Based AI Operating System Assistant",
    license="Proprietary",
)
