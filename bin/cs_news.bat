@echo off
rem echo press any key to start
rem pause
echo running....
cd ..
scrapy crawl cs_news -s CLOSESPIDER_TIMEOUT=3600 -s LOG_FILE=/logs/cs_news_%date:~0,4%-%date:~5,2%-%date:~8,2%.log
rem echo press any key to exit
rem pause
exit