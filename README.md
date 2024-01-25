# WPILib-Python-Test

Robot code for the FRC 2024 "Crescendo" competition.

**External Software**

_It is recommended to develop using Windows 10/11, since as of 1/25/2024 there is no native MacOS support for FRC Game Tools/Radio Configuration_

- [WPILib 2024](https://github.com/wpilibsuite/allwpilib/releases/tag/v2024.2.1) (Not needed for python development)
- [FRC Game Tools 2024](https://www.ni.com/en/support/downloads/drivers/download.frc-game-tools.html#500107) (Windows ONLY!)
- [FRC Radio Configurstion Utility 2024](https://firstfrc.blob.core.windows.net/frc2024/Radio/FRC_Radio_Configuration_24_0_1.zip) (Windows ONLY!)
  - [Israel Version](https://firstfrc.blob.core.windows.net/frc2024/Radio/FRC_Radio_Configuration_24_0_1_IL.zip)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)
  - NOTE: If Anaconda is already on your system, miniconda is not needed!
## Setup

To setup this code on your computer for development, follow the steps below:

**Windows**
- Make sure all software is downloaded and installed (check "External software")
- Clone the repository
- Open **Anaconda Powershell Prompt** and navigate to the parent directory in which the repository is stored on your local machine (NOTE: You will need to use Unix commands like `cd` to navigate in the Anaconda Powershell Prompt)
- Build a new conda environment from the **WINDOWS SPECIFIC** environment YAML file for windows:
  - `conda env create -f environmentwindows.yaml`
  - `conda activate WPILib-Python-Test`

**MacOS/Unix/GNU**
- Optionally download WPILib 2024, just know it is not needed for python development
- Download and install miniconda (SKIP this step if you already have anaconda installed on your Mac)
- Clone the repository
- Open **Terminal** and navigate to the parent directory in which the repository is stored on your local machine
- Build a new conda environment from the **MACOS SPECIFIC** environment YAML file:
  - `conda env create -f environmentunix.yaml`
  - `conda activate WPILib-Python-Test`
