<img src="https://miro.medium.com/v2/resize:fit:4800/format:webp/1*pCu3qdwrNTUcCm553x46gg.png" width="30%" alt="hackerman-flipper">
<br>

# Flipper Scripts & Writeups

Just shitposting useless tools that are useful for me,
maybe for others as well ¯\_(ツ)_/¯

## Tools
### patcher.py 
patch custom firmwares to preserve my own custom tweaks after flashing. <br> 
#### Currently supports:

- Patching the name of the dolphin in the firmware.
- Patching the points of the Flappy Bird game in the firmware.
- Building the firmware with custom arguments.
```bash
python patcher.py -p <path_to_firmware> -f <firmware_type> -b -a <build_args>
```

### levelup.py
#### patch .dolphin.state file to increase icount (xp) and level up the Flipper Dolphin levels

[hacking-the-hackers-tool-pwning-flipper-zero](https://medium.com/@60noypearl/hacking-the-hackers-tool-pwning-flipper-zero-s-levels-for-fun-1dd16847da5a)

```bash
python dolphin_state_patcher.py <file_path> <xp_value>
```


### /etc/
- bytes.py - Convert num to bytes little endian etc. 

## Writeups
[hacking-the-hackers-tool-pwning-flipper-zero](https://medium.com/@60noypearl/hacking-the-hackers-tool-pwning-flipper-zero-s-levels-for-fun-1dd16847da5a)






## Cheatsheet & tips

### Building Firmware
### Compile everything for development

```sh
./fbt FIRMWARE_APP_SET=debug_pack updater_package
```

### Compile everything for release + get updater package to update from microSD card

```sh
./fbt COMPACT=1 DEBUG=0 updater_package
```

Check `dist/` for build outputs.

Use **`flipper-z-{target}-update-{suffix}.tgz`** to flash your device.



### Updating Firmware

#### **Replace (CURRENT VERSION) with version that you downloaded from releases**
- Unpack `flipper-z-f7-update-(CURRENT VERSION).tgz` (or `.zip`) into any free folder on your PC or smartphone
- You should find folder named `f7-update-(CURRENT VERSION)` that contains files like `update.fuf`, `resources.tar` and etc..
- Remove microSD card from flipper and insert it into PC or smartphone (you can skip this step and upload all files using qFlipper)
- Create new folder `update` on the root of the microSD card and move folder that you previously extracted from archive - `f7-update-(CURRENT VERSION)` into `update` on microSD card
- So result should look like `update/f7-update-(CURRENT VERSION)/` with all files in this folder on microSD card, remember iOS default Files app doesn't show all files properly (3 instead of 6), so you need to use another app for unpacking or use PC or Android
- Verify that all files are present on your microSD card
- After all you need to insert microSD card back into flipper, navigate into filebrowser, open this file 
`update/f7-update-(CURRENT VERSION)/update.fuf`
- Update will start, wait for all stages
- Done
![manual](https://user-images.githubusercontent.com/40743392/235006410-19eaf58e-2425-4e8e-8ec9-973bda362c47.png)

[source](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#update-firmware)
