# WMC-Battery

Python reimplementation of the WMC battery described in Lewandowsky, Oberauer, Yang, & Ecker (2010), Behavior Research Methods.

## Install psychopy

### Ubuntu 20.04

```
pip install psychopy==2020.2.10 pygame numpy pandas scipy dotmap pyyaml
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython
sudo apt install libxcb-xinerama0
```

For Chinese font support:

```
sudo apt install fonts-noto-cjk
```

### Mac OS

```
pip install psychopy==2020.2.10 pygame wxPython numpy pandas scipy dotmap pyyaml
```

For Chinese, please download and install the required font package 'Noto Serif CJK SC': https://www.google.com/get/noto/

The support for font install : https://www.google.com/get/noto/help/install/



### Windows

```
pip install psychopy==2020.2.10 pygame wxPython numpy pandas scipy dotmap pyyaml
```

For Chinese, please download and install the required font package 'Noto Serif CJK SC': https://www.google.com/get/noto/

The support for font install : https://www.google.com/get/noto/help/install/


## Run WMC Battery

```
python3 wmc.py
```


You can quit the experiment by pressing `F12`.


It is advised to mark the arrow-keys on your physical keyboard for the *Operation Span* and *Sentence Span* tasks. You can configure the keys in the `yaml`-config files in the `config` folder (`key_map` field).