# pyPicoTool

## Overview
This library allows you to interact with the Raspberry Pi [picotool](https://github.com/raspberrypi/picotool) utility in a more controlled way.

You can get information about connected devices, reboot one of the device, load firmware to a device, save the flash contents of a device to a file, and reboot a device.

## Examples
See examples for all the functions in the [examples](examples) directory.

## Installation

For the library to work you need to have `picotool` in your PATH.


To install the library you can use the `setup.py` script:

`python setup.py install`

### Building picotool

See the [picotool readme](https://github.com/raspberrypi/picotool#readme) for more details but the short version is:

```
git clone https://github.com/raspberrypi/pico-sdk.git
export PICO_SDK_PATH=`pwd`/pico-sdk

git clone https://github.com/raspberrypi/picotool.git
cd picotool
mkdir build
cd build
cmake ..
make
export PATH=$PATH:`pwd`

```
