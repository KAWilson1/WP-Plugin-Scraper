#Author: Kyle Wilson, Noah Coomes
#Init: 1/4/2018
#Last Updated: 1/4/2018

from urllib.request import urlopen
import re

def readFile(path):
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def formatURL(url):
    if type(url) != str:
        raise Exception("Invalid data type passed to formatURL")

    if url[:7] == "http://" or url[:8] == "https://":
        return url
    
    if url[:3] == "www":
        url = "http://" + url
        return url

    return "http://www." + url

def getDomainName(url):
    if type(url) != str:
        raise Exception("Invalid data type passed to getDomainName")

    if url[:11] == "http://www.":
        return url[11:]
    if url[:12] == "https://www.":
        return url[12:]
    
    if url[:7] == "http://":
        return url[7:]
    if url[:8] == "https://":
        return url[8:]

    return url

def scrapeLinks(url):
    cleanURL = formatURL(url)
    
    if type(cleanURL) != str:
        raise Exception("Invalid argument passed to scrapeLinks")
    
    website = urlopen(cleanURL)

    source = website.read()
    source = source.decode('UTF-8')

    # Find text similar to 'http(s)://...'
    links = re.findall("'(https?://.*?)'", source)
    return links

def getPlugins(linkList, domainName):
    #tuple list of plugin names and versions
    toReturn = []

    for i in range(len(linkList)):
        splitLink = linkList[i].split("/")

        #get version
        for ele in splitLink:
            if "ver=" in ele:
                currVersion = ele.split("=")[len(ele.split("="))-1]

        #get plugin name
        if splitLink[2] == domainName:
            if "plugins" in splitLink:
                refIdx = splitLink.index("plugins")
                try:
                    toReturn.append([splitLink[refIdx+1], currVersion])
                except UnboundLocalError:
                    toReturn.append([splitLink[refIdx+1], "N/A"])
    return toReturn

def getThemes(linkList, domainName):
    #tuple list of theme names and versions
    toReturn = []

    for i in range(len(linkList)):
        splitLink = linkList[i].split("/")

        #get version
        for ele in splitLink:
            if "ver=" in ele:
                currVersion = ele.split("=")[len(ele.split("="))-1]

        #get theme name
        if splitLink[2] == domainName:
            if "themes" in splitLink:
                refIdx = splitLink.index("themes")
                try:
                    toReturn.append([splitLink[refIdx+1], currVersion])
                except UnboundLocalError:
                    toReturn.append([splitLink[refIdx+1], "N/A"])
    return toReturn

def getInstallationDir(linkList):
    if linkList[0].split("/")[3] == "wp-content" or linkList[0].split("/")[3] == "wp-admin":
        return "N/A"
    
    return linkList[0].split("/")[3]

def removeDuplicates(tupleList):
    toReturn = []

    for myTuple in tupleList:
        if myTuple not in toReturn:
            toReturn.append(myTuple)
    return toReturn

def printInfo(outputName, websitePackages):
    if outputName[-4:] != ".txt":
        outputName += ".txt"

    f = open(outputName, 'w')

    for package in websitePackages:
        f.write("Website: " + package[0] + "\n")
        f.write("Dir: " + package[1] + "\n")

        f.write("Plugins:\n")
        for entry in package[2]:
            f.write(entry[0] + " -> " + entry[1] + "\n")

        f.write("Themes:\n")
        for entry in package[3]:
            f.write(entry[0] + " -> " + entry[1] + "\n")
        f.write("\n")

    f.close()


        
    
