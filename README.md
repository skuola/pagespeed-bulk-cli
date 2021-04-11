# Pagespeed bulk CLI
Script to get Web Vitals Pagespeed from URLs taken from a csv file  

## Requirements
- python 3 (tested on python 3.6.9)  
- lib request (`pip3 install requests`)  
- lib pandas (`pip3 install pandas`)  

## API key
Create your pagespeed key here: https://console.developers.google.com/apis/credentials?authuser=0  
then assign it to `pagespeedKey` variable in the python script  

## USAGE
```bash
python3 pagespeed-bulk.py -i url.csv -o pagespeed-result.csv
```
