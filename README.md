# ITA (Image to ASCII)

## Description
A compiled Python script that transfers image into text (ASCII). 

**Dependencies**
- Python (3 or above)
- Pillow (11.0.0 or above)

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
The config.json file is located in `~/.config/image-to-ascii/config.json`. There are multiple rules when configuring this.

TODO