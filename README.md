# Bilibili-video-downloader


[Bilibili-video-downloader](https://you-get.org/) is a simple Bilibili video and danmaku downloader with GUI.
Currently only support GUI for Mac OS.
For Windows user, only terminal python run is available.

**Note:**
* Some videos cannot be downloaded due to region's difference. Only who lives in mainland, China could download videos such as bangumi and films.
* Those live in foreign country could use global proxy setting to download those mentioned videos.
* Currently could only download one part from the target website if the video has multiple parts.
* Currently could only download the highest quality from the website. If one want to download membership-quality videos(e.g. 1080P60, 4K), one should enter the cookie which will talked in the following instruction.




## Installation

### Prerequisites

**Note:**
The following dependencies are necessary for Windows user(not using Executable):

* **[Python](https://www.python.org/downloads/)**  3.2 or above
* **[FFmpeg](https://www.ffmpeg.org/)** 1.0 or above

### Option 1: Download from GitHub
This is the recommended way for all developers, even if you don't often code in Python.

```
$ git clone https://github.com/sunkashing/BiliBili-video-downloader
```



## Getting Started

### Open application GUI


#### Mac user

Go to `Bilibili-video-downloader/dist/` folder, and click `video_downloader.app` to run application.


#### Windows user

Open a terminal, after installing all required libraries and packages, type

```sh
$ python3 video_downloader.py
```



### Download a video

#### Step1

Open a target Bilibili video site from browser, and paste the url to the `BV number:` input field


#### Step2 (optional)

If you are a membership(大会员) and want to download those membership-quality videos(e.g. 1080P60, 4K).
Go to the target video's site and open the developer tool of the browser. Choose `Network` menu from the menubar and choose `Headers` from the submenu.
If the `Has blocked cookies` is enabled, disable it. Refresh the page, find a package whose name is same as the video's BV number(usually the top one in the `Name` column) and clicked on it.
Go to `Request Headers` and find `Cookie` field. Copy the value of it(Do not include `Cookie:`) and paste it to the GUI's `Cookie(optional):` field.


#### Step3

Choose a saving directory of the downloaded video by clicking `Choose Directory`.


#### Step4(optional)

If you want to improve the downloaded video's fps(if it is not 60fps originally), check the `60fps boost`.

**Note**
* This option will take a long time to run, if your computer's hardware is not good, do not check it.


#### Step5

Click `Download` button and wait for completion!


#### Step6

Open the downloaded video, if the player does not load the `.ass` file automatically, you can load the generated `.ass` file to the video.(Most player should support it)
Watch your video with danmaku and have fun!!!




## Authors

Made by [@sunkashing](https://github.com/sunkashing).

Inspired by [@soimort](https://github.com/soimort/you-get) and [@m13253](https://github.com/m13253/danmaku2ass).
