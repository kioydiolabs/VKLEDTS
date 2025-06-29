# Contribution Instructions/Information


### General
Although this repository contains tests that I have made for my usecase and other KioydioLabs project, contributions are welcome.
You are free to open pull requests and submit any tests you might think are useful.
You must test them thoroughly first and be sure they work fairly well.

Generally, make sure that you do not hard-code any VISA resources, and use the visares.py file.
Also, do not hard-code a lot of values that may change. Prefer asking the user with an input().

### Instrument Support
**You are also limited to the following instruments that are supported by psytestbench library:**

```
- Siglent SPD3303x power supplies
- Rigol DS1000Z/MSO1000Z series oscilloscopes (like the classic DS1054z)
- Unitrend Uni-T UTG9xx signal generators (tested on the UTG962)
- Unitrend Uni-T UT880x multi-meters (test on UT8804N, should work on all 8000 series?)
```
_(according to https://github.com/psychogenic/psytestbench/blob/main/README.md#current-instruments-supported)_
However you may be able to contribute to the library first if your instrument is not supported.

_Professional lab instruments manufacturers such as Keysight, R&S, Tektronix or Teledyne Lecroy, release their own
advanced software and scripts for them should not be added to this repository. The repository contains scripts
for lower-end instruments which do not have their own software, or at least software that works well._

### Structure and Other

Your script should be placed in a new directory with a short but descriptive name.
Inside the directory, include a README.md file, in the format of the [EXAMPLESCRIPTREADME.md](EXAMPLESCRIPTREADME.md) file.

THE FILENAME OF THE SCRIPT MUTS CONTAIN THE EXACT MODEL OF THE INSTRUMENT.
See [File Naming](#file-naming) below.

If you are adding a script for an instrument, for which there are no scripts in this repository yet,
update the repository's README.md to include the new instrument under the 'Supported Instruments' heading.

### File Naming

The file should have the instruments full model.

**Prepend the model name with the manufacturer letter code as follows**

| Manufacturer   | Letter Code |
|----------------|-------------|
| Rigol          | RG          |
| Unitrend UNI-T | UT          |
| Siglent        | SG          |