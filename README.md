# WMC-Battery

Python reimplementation of the WMC battery described in Lewandowsky, Oberauer, Yang, & Ecker (2010), Behavior Research Methods.

## Installation

### Ubuntu 20.04
You may need to put `.local/bin` in your `PATH` by adding this to your `.bashrc` in your home folder:
```
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

```
sudo apt-get install psychopy python3-pip python3-wxgtk-webview4.0 libxcb-xinerama0

pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython==4.1.1
```

For Chinese font support:

```
sudo apt-get install fonts-noto-cjk
```

To run the


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

### Ubuntu 20.04


```
python3 wmc_ubuntu.py
```


### MacOS


```
python3 wmc_mac.py
```


### Windows


```
python3 wmc_windows.py
```


You can quit the experiment by pressing `F12`.


It is advised to mark the arrow-keys on your physical keyboard for the *Operation Span* and *Sentence Span* tasks. You can configure the keys in the `yaml`-config files in the `config` folder (`key_map` field).

## Test language files

You can test your language files by running the following command:

```
python3 test_language.py
```

You will move through all experiment messages, instruction pages, a summary for sentence span sentences and all sentence span sentences with the respective label. For the sentence summary, moving on is possible only after one second has passed to prevent accidental skipping.
