# VLKEDTS


> [!IMPORTANT]
> This repository is in extremely early stages.
> If you are going to use the scripts here on your own instruments,
> it's probably a good idea to backup the instrument's configuration
> since the scripts may mess it up. Scripts may also make the instrument
> unstable, for instance if they don't disconnect properly you may need
> to restart the instrument.

This repository contains Python scripts, which are used to test devices during embedded development, using VISA-compatible instruments.

For communication with the instruments, the https://github.com/psychogenic/psytestbench library is used.
You should really check it out, since it's the only library that's actually useful and not trash!

## Structure
Each test script is in its own directory.
Every test directory, contains test scripts for different instruments.
Also included is a README.md file in each directory, which explains what the test script does.

## Supported Instruments
At the moment this repository only contains scripts for the following instrument(s):
- Rigol DS1104Z Digital Storage Oscilloscope

In the future more instruments might be added.

## Contributing
Too long to include here. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the GNU General Public License v3.0 or later.  
See the [LICENSE](./LICENSE) file for details.