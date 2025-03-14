REQUIREMENTS:

1) BeautifulSoup - parsing html
2) requests - for addition scraping, like number of seasons
3) pycryptodome - for deciphering
4) ffmpeg - don't forget to specify the path in process.py
5) puppeteer, Node.js


This script allows you to download any movie or any episode of any series.

This script finds HLS link on popular streaming platform, encryption key, downloads all . ts segments and deciphers them
then merges those files in order using ffmpeg to .mp4 format.
Sometimes it might not work due to certain streaming service not being available, I have figured it out, but it's
yet to be implemented.

Closing browser or rerunning the script can usually fix some issues.
If some error happens make sure you delete captured url text file in script folder.
