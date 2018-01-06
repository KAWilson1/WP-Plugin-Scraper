#Author: Kyle Wilson, Noah Coomes
#Init: 1/4/2018
#Last Updated: 1/6/2018
#Purpose: Crawl a list of wordpress websites and pull relevant information from them

from WP_Scraper_Functions import * 

websiteURLs = readFile("websites_to_scrape.txt")
websitePackages = []

for i in range(0, len(websiteURLs)):
    formattedURL = websiteURLs[i]
    domainName = getDomainName(formattedURL)

    print("Reading from: " + domainName)
    
    links = scrapeLinks(formattedURL)

    plugins = removeDuplicates(getPlugins(links, domainName))
    themes = removeDuplicates(getThemes(links, domainName))
    installDir = getInstallationDir(links)

    websitePackages.append([domainName, installDir, plugins, themes])

printInfo("output", websitePackages)
