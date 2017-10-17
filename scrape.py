from bs4 import BeautifulSoup
import sys
import os
import requests
import re

def main():
    baseUrl = 'https://keliapu.net/data/'
    startYear = int(sys.argv[1])
    startMonth = int(sys.argv[2])
    print("Beginning data collection, starting from " + str(startYear) + "/" + str(startMonth))
    dataDirs = getLinksWithForm(baseUrl, re.compile(r'\d{4}-\d{2}/'))
    wantedDirs = filterDirs(dataDirs, startYear, startMonth)
    print(wantedDirs)
    fileAddrs = getCsvLinks(baseUrl, wantedDirs)
    downloadFiles('https://keliapu.net/data/', 'data/', fileAddrs)
    print("Great success!")

# Takes url and regex, return list of links on url where hrefs satisfy the regex
def getLinksWithForm(url, regex):
    httpRes = requests.get(url)
    soup = BeautifulSoup(httpRes.content, 'html.parser')
    allLinks = list(map(lambda link: link.attrs['href'], soup.find_all('a')))
    return list(filter(regex.search, allLinks))

# Takes list of strings where first 4 letters form an integer and returns all
# members that are greater than startYear
def filterDirs(dirs, startYear, startMonth):
    return [d for d in dirs if int(d[:4]) > startYear or (int(d[:4]) == startYear and int(d[5:7]) >= startMonth)]

# Takes a url and a list of URLs and returns a dictionary of URL: [url1,...,urln]
# links to .csv-files on those URLs
def getCsvLinks(baseAddr, dirs):
    return {d: getLinksWithForm(baseAddr + d, re.compile(r'^.*\.csv$')) for d in dirs}

# Takes baseurl, list of strings(filename) and a string(dirname),
# loads all baseurl + filename and puts them into dir/filename
def downloadFiles(baseUrl, destFolder, dirs):
    for folder, files in dirs.items():
        assureFolderExists(destFolder + folder)
        for file in files:
            filename = folder + file
            print("Downloading " + filename)
            content = requests.get(baseUrl + filename).content
            with open(destFolder + filename, 'wb+') as f:
                f.write(content)

def assureFolderExists(path):
    if not os.path.exists(path):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as err:
            raise
main()
