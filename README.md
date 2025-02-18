# ITA (Image to ASCII)

## Description
A compiled Python script that transfers image into text (ASCII). 

**Dependencies**
- Python (3 or above)
- Pillow (11.0.0 or above)

<img src="">

## Installation
#### [1] Download image-to-ascii from github
```shell
git clone https://github.com/sh1d0re/image-to-ascii
```

#### [2] Choose your operating OS (macOS or Linux), and rename it to `ita`.

<details><summary><b>macOS</b></summary>

```shell
sudo mv ita-macos ita
```
</details><details><summary><b>Linux</b></summary>

```sh
sudo mv ita-linux ita
```
</details><details><summary><b>Don't see your OS?</b></summary>

We are either currently working on it, or ended support for a reason. However, you can compile the script by yourself!
Python compilers such as [Nuitka](https://nuitka.net/), allows easy installation and operation. Compile the `main.py` file to an executable, and rename it to `ita`, and you can simply go to step 3.
</details>

#### [3] And then, execute the following:
```shell
sudo cp ita /usr/local/bin
sudo chmod +x /usr/local/bin/ita
mkdir ~/.config/image-to-ascii/
cp config.json ~/.config/image-to-ascii
rm -rf image-to-ascii # Optional
```

## How to use
> **Format:** `ita [image file name (.png / .jpg / etc.)]`

> **Example:** `ita target.png`

## Configuring
If you are interested in configuring your ita (image-to-ascii), do the following:
The config.json file is located in `~/.config/image-to-ascii/config.json`. There are multiple rules when configuring this. The contents of the json file are structured as the following:

```json
{
    "$comment": "If you are willing to configure this program, please refer to the README.md file to prevent any bugs.",

    "brightnessWeight": "BT.601",  
    "fillCharacters": ["  ", "..", ".:", ":;", ";;", "==", "**", "*$", "$$", "@@", "##"],
    "splitter": " "
}
```

> ### BrightnessWeight
The `brightnessWeight` key, controls the method of the RGB to Luma conversion. You can change this, by replacing it with your desired conversion method:
```json
{
    "BT.601": [
        0.897,
        1.761, 
        0.3423
    ],
    "BT.709-6": [
        0.6378,
        2.1456,
        0.2166 
    ],
    "NoBias": [
        1,
        1,
        1 
    ],
    "SmallBias": [
        0.9, 
        1.5, 
        0.6 
    ]
}
```

You can also provide your own custom RGB to luma conversion methods, by entering a list type variable. For isntance:
```json
{
    ...
    "brightnessWeight": [
        0.6,
        2.1,
        0.3
    ]
    ...
}
```

> ### FillCharacters
The `fillCharacters` key, would use its contents to use the texts in the list, to fill in pixel chunks in the selected image. You can configure it with other characters, for instance:
```json
{
    ...
    "fillCharacters": ["　", "土", "木", "火", "水", "日", "月", "金"]
    ...
}
```
You can also use escape sequences (ANSI), to change text both fore and background colors.

> ### Splitter
The `splitter` key, would be used to determine the margins between the fillCharacters. 