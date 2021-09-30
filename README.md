# miditell
A helper script for getting instrument names out of midi files

## Requirements

```
pip install git+https://github.com/vishnubob/python-midi@feature/python3 sf2_loader
```

## Usage

```
$ miditell -i song020.mid
  0 -   0: Type 0 @0x27b2c0
  0 -   1: Type 0 @0x27b2cc
  0 -  18: Type 0 @0x27b398
  0 -  29: Type 0 @0x27b41c
  0 -  34: Type 0 @0x27b458
  0 -  35: Type 0 @0x27b464
  0 -  36: Type 0 @0x27b470
  0 -  37: Type 0 @0x27b47c
  0 -  38: Type 0 @0x27b488
  0 -  40: Type 0 @0x27b4a0
  0 -  54: Type 0 @0x27b548
  0 -  61: Type 0 @0x27b59c
  0 -  62: Type 0 @0x27b5a8
  0 - 101: Type 0 @0x27b77c
  0 - 102: Type 0 @0x27b788
  0 - 123: Type 128 @0x27b884
```