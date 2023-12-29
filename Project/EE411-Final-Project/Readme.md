# EE411 Final Project


## Overview

`50-SF_decoder.py` used for decoding and restoring to the original image.
`50-SF.txt` is the encoded file.
`50-SF.jpg` is the decoded file.
[`utils`](https://github.com/jeter1112/dna-fountain-simplified/tree/main/py2ImagDecode/utils) comes from https://github.com/jeter1112/dna-fountain-simplified/tree/main/py2ImagDecode/utils.


---

## Usage

> Prerequisite

1. install python2.7.18
2. install numpy,reedsolo,tqdm. One installation method：`$pip2 install numpy reedsolo tqdm`
3. run `50-SF_decoder.py` in terminal with `$ /bin/python2 50-SF_decoder.py`


## Results

![50-SF.jpg](50-SF.jpg)

```bash
INFO:root:After reading 1821 lines, we finished decoding!
INFO:root:Restoring the picture now!
100%████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1494/1494 [00:00<00:00, 860163.37it/s]
INFO:root:MD5 is b4c92ee632d5be073e1fc0a16902bd7c
INFO:root:Done!
```

