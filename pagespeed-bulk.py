#!/usr/bin/python3

# Script to get Web Vitals Pagespeed from URLs taken from a csv file, one URL per line
#
# Usage:
# python3 pagespeed-bulk.py -i url.csv -o pagespeed-result.csv
#
# Requirements:
# python3: tested on python 3.6.9
# lib request: pip3 install requests
# lib pandas: pip3 install pandas

import pandas as pd
import requests
import sys, getopt

pagespeedUrl = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
# Create your pagespeed key from https://console.developers.google.com/apis/credentials?authuser=0 and insert it here:
pagespeedKey = ''

def main(argv):
    inputfile = ''
    outputfile = ''
    help_string = 'pagespeed-bulk.py -i <inputcsvfile> -o <outputcsvfile>'

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == '' or outputfile == '':
        print(help_string)
        sys.exit(2)

    df = pd.read_csv(inputfile, header = None)
    output_data = {'url': [], 'strategy': [], 'score': [], 'cls': [], 'si': [], 'lcp': [], 'fcp': [], 'tbt': [], 'tti': []}

    for url in df[0]:
        try:
            data = runPagespeed(url, 'mobile')
            appendToArrayDict(output_data, data)
            data = runPagespeed(url, 'desktop')
            appendToArrayDict(output_data, data)
        except requests.exceptions.HTTPError as err:
            print(err.response.status_code, ' - ', url)
            continue
        except requests.exceptions.InvalidSchema as err:
            print("Error: invalid schema - ", url)
            continue
        except requests.exceptions.InvalidURL as err:
            print("Error: invalid URL - ", url)
            continue
        except requests.exceptions.MissingSchema as err:
            print("Error: missing schema - ", url)
            continue
        except requests.exceptions.ConnectionError as err:
            print("Error: connection error - ", url)
            continue

    df = pd.DataFrame(output_data, columns = ['url', 'strategy', 'score', 'cls', 'si', 'lcp', 'fcp', 'tbt', 'tti'])
    df.to_csv(outputfile)


def runPagespeed(url, strategy):
    payload = {'key': pagespeedKey, 'url': url, 'category': 'performance', 'strategy': strategy}
    response = requests.get(pagespeedUrl, params = payload)
    response.raise_for_status()
    jsonResponse = response.json()

    data = {}
    data['url'] = url
    data['strategy'] = strategy
    data['score'] = round(jsonResponse['lighthouseResult']['categories']['performance']['score'] * 100)
    # For each field instead of the 'displayValue' we could take the value 'numericValue', formatting it appropriately
    data['cls'] = jsonResponse['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
    data['si'] = jsonResponse['lighthouseResult']['audits']['speed-index']['displayValue']
    data['lcp'] = jsonResponse['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
    data['fcp'] = jsonResponse['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
    data['tbt'] = jsonResponse['lighthouseResult']['audits']['total-blocking-time']['displayValue']
    data['tti'] = jsonResponse['lighthouseResult']['audits']['interactive']['displayValue']

    print("{:s} [{:s}]: {:d}".format(data['url'], data['strategy'], data['score']))

    return data


def appendToArrayDict(dictionary, data):
    dictionary['url'].append(data['url'])
    dictionary['strategy'].append(data['strategy'])
    dictionary['score'].append(data['score'])
    dictionary['cls'].append(data['cls'])
    dictionary['si'].append(data['si'])
    dictionary['lcp'].append(data['lcp'])
    dictionary['fcp'].append(data['fcp'])
    dictionary['tbt'].append(data['tbt'])
    dictionary['tti'].append(data['tti'])

    return dictionary


if __name__ == "__main__":
    main(sys.argv[1:])
