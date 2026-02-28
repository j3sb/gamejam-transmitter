This is a copy of the hid_composite example from TinyUSB (https://github.com/hathach/tinyusb/tree/master/examples/device/hid_composite)
showing how to build with TinyUSB when using the Raspberry Pi Pico SDK

# Build

install the pico-sdk

```
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init

```

and set the env path

```
export PICO_SDK_PATH=$HOME/pico-sdk
```

then build


```
mkdir build && cd build
cmake ..
cmake --build .
```

then flash with

```
picotool load dev_hid_composite.uf2
```

you might want to add the following udev rule to /etc/udev/rules.d/50-pico.rules to flash without bootsel

```
# Raspberry Pi Pico
SUBSYSTEM=="usb", ATTR{idVendor}=="2e8a", MODE="0666"
```

or in nix:

```
services.udev.extraRules = ''
    # Raspberry Pi Pico
    SUBSYSTEM=="usb", ATTR{idVendor}=="2e8a", MODE="0666"
  '';
```