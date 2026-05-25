# Android Build Guide

This project is prepared for Android packaging with Buildozer.

## Recommended Linux

For this project, use `Ubuntu-22.04` in `WSL2`.

Install it from Windows PowerShell:

```powershell
wsl.exe --install Ubuntu-22.04
```

## Important

Buildozer works on Linux and macOS, and on Windows through WSL.
On this machine, `wsl --status` previously reported that WSL 2 could not start because virtualization was disabled.

Before building:

1. Enable virtualization in BIOS/UEFI.
2. Enable Windows features:
   - `Virtual Machine Platform`
   - `Windows Subsystem for Linux`
3. Install and launch `Ubuntu-22.04`.

## Build Steps In Ubuntu / WSL

Open `Ubuntu-22.04`, then install the required packages:

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake
python3 -m pip install --user --upgrade buildozer
echo 'export PATH=$PATH:~/.local/bin/' >> ~/.bashrc
source ~/.bashrc
```

Copy the project into the WSL filesystem before building. This is faster and avoids NTFS path issues:

```bash
cp -r /mnt/c/Users/Public/shooter ~/shooter
cd ~/shooter
buildozer -v android debug
```

The first build takes a long time because Buildozer downloads the Android SDK, NDK, and other toolchain components.

When it succeeds, the APK will be in:

```text
~/shooter/bin/
```

## Build In GitHub Actions

This repo also includes a GitHub Actions workflow at `.github/workflows/android-build.yml`.

After you push the repository to GitHub:

1. Open the `Actions` tab.
2. Run the `Android APK` workflow manually, or let it run on push/pull request.
3. Download the `android-apk` artifact from the workflow run summary.

## Install On Android

For a quick manual install:

1. Copy the generated APK from `~/shooter/bin/` to Windows or directly to your Android phone.
2. Allow installs from unknown sources on the device if needed.
3. Tap the APK and install it.

For USB deployment later, WSL does not directly handle USB device access well, so use `adb` from Windows after copying the APK out of WSL.

## Notes

- `buildozer.spec` already includes `json` files, so `data/players.json` will be packaged.
- The app is currently portrait-only.
- If you add sounds later, update `source.include_exts` to include their extensions such as `wav`, `ogg`, or `mp3`.
