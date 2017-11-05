# ref_parser
Reference parser that extracts references from all kinds of files. It uses Google Scholar engine to obtain corresponding BibTex info. 
## Thanks to
* [gscholar](https://github.com/venthur/gscholar)
* [textract](https://github.com/deanmalmgren/textract)
## Requirements
* python
* textract
## Installation
### Install "textract" package
#### Ubuntu / Debian
```
apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
pip install textract
```
It may also be necessary to install "zlib1g-dev" on Docker instances of Ubuntu. 
#### OSX
```
brew cask install xquartz
brew install poppler antiword unrtf tesseract swig
pip install textract
```
Then you are good to go! (You might need other packages, please follow the error messages.)

## Usage
### Before use
Update the cookies.txt file before use. You can get the cookies by opening [Google Scholar](scholar.google.com) with you browser, search for any paper in the search bar, get its BibTex info, then use your browser's "inspect elements" function, navigate to "Network" -> "Headers". Under "Response Headers" section, you may find your cookies info. Copy and paste it to your cookies.txt file. Always use the cookies with "GSP" parameter. 

If you get blocked, open your browser and search for some paper in Google Scholar, try to pass the "I'm not a bot" test, check your cookies again, you'll find a new term "GOOGLE_ABUSE_EXEMPTION". Update your cookies.txt file with the new cookie, and you are back on track again. 

### How to use
It's simple:
```
python ref_parser.py input output
```
Enjoy!
## Important information
Remember, Google only allows a single ip to get couple hundreds of bibtex info PER DAY. If you parse too fast in a short amount of time, you'll be banned for a day. Use the service moderately, and always set an interval between each query. Default interval setting is 20-30 seconds. Do not make it less than 10 seconds, users are responsible for use of this script. 


