# Web Crawler that takes KEYPHRASE and finds unique and relevant WebPages 
# using BFS approach to crawl web pages

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
from urllib.parse import urlparse
from time import sleep

class MyHtmlParser(HTMLParser):
    def __init__(self, keyPhrase):
        super().__init__()
        self.keyPhrase = keyPhrase

    
    def handle_starttag(self, tag, attrs):

        # fetch Anchor tag and its Href attribute with its value
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)

                    # parsing URL into 6 components
                    o = urlparse(newUrl)
                    
                    # netloc represents Networks Location # basically checking whether it is English Wikipedia page    
                    if o.netloc == 'en.wikipedia.org':
                        if newUrl.find('.org/wiki/') >-1:
                            
                            # avoiding "Main Page" of Wikipedia
                            if newUrl.find('.org/wiki/Main_Page/') == -1:
                                if newUrl.find(':', 10) == -1:
                                    if newUrl.find('#', 10) == -1:

                                        # adding Time delay of 1 second to access wikipedia page.
                                        #sleep(1)

                                        # focused crawling
                                        # Get data of the fetched link and check whether it is relevant to given keyword
                                        # following code is slowing down WebCrawler
                                        response_new = urlopen(newUrl)
                                        htmlBytes_new = response_new.read()
                                        htmlString_new = htmlBytes_new.decode("utf-8")
                                        # converting to lowercase and comparing with kepPhrase (which was converted to lowercase)
                                        htmlString_new = htmlString_new.lower()
                                        
                                        if htmlString_new.find(self.keyPhrase) >-1:
                                            self.links = self.links + [newUrl]
                                        

    
    def getLinks(self, url):
        
        self.links = []
        
        self.baseUrl = url
        
        response = urlopen(url)

        htmlBytes = response.read()
            
        htmlString = htmlBytes.decode("utf-8")
        
        self.feed(htmlString)

        return htmlString, self.links
        

def WebCrawler(url, keyPhrase):

    keyPhrase = keyPhrase.lower()
    maxLinks = 1000
    UniqueLinksFetched = [url]
    pagesCrawled = 0

    depth = 1

    # all web pages at same depth are kept in this list
    # this list is later used at Queue implementing Breadth First Search
    depth_queue = [url]
    depth_index = len(UniqueLinksFetched)
    
    while depth <= 5 and UniqueLinksFetched != [] and len(UniqueLinksFetched) < maxLinks:

        # This while loop handles depth criteria    
        while len(depth_queue) != 0 and UniqueLinksFetched != [] and len(UniqueLinksFetched) < maxLinks:

            pagesCrawled = pagesCrawled +1
            url = depth_queue.pop(0)
            
            
            try:
                print("=============================================")
                print("Pages Crawled : ",pagesCrawled, "\nCurrently Crawling: ", url)   
                parser = MyHtmlParser(keyPhrase)
                data, links = parser.getLinks(url)
                
                temp = len(UniqueLinksFetched) 
                UniqueLinksFetched = UniqueLinksFetched + links

                # fetching unique links by converting to SET
                UniqueLinksFetched = list(set(UniqueLinksFetched))
                temp2 = len(UniqueLinksFetched) - temp

                # fetching only first 1000 links
                if len(UniqueLinksFetched) >= maxLinks:
                    UniqueLinksFetched = UniqueLinksFetched[0:maxLinks]
    
                print("Relevant Links fetched in current page:", len(links))
                print("Unique Links fetched in current page:", temp2)
                print("Total No. of unique links fetched :", len(UniqueLinksFetched))

                
                
            except:
                print("Failed!!! \n Error Occured!!!")
                # print(format(e.errno, e.strerror))

        try:
            depth_queue =  UniqueLinksFetched[depth_index : len(UniqueLinksFetched)]
            depth_index = len(UniqueLinksFetched)
            depth += 1

            if depth <=5 and UniqueLinksFetched != [] and len(UniqueLinksFetched) < maxLinks:
                print("=============================================")
                print("Entering depth :",depth)
        except:
            print("Failed!!!")

    if len(UniqueLinksFetched) >= maxLinks:
        print("1000 unique links have been fetched")
    elif UniqueLinksFetched == []:
        print("all relevant WebPages have been crawled")
    else:
        print("WebPages at depth 5 have been crawled")

                
    print("Crawling Stopped at depth : ",depth-1)
    print("Total Links Fetched : ",len(UniqueLinksFetched))
    print("Fetched Links : ")
    print("=============================================")
    print(UniqueLinksFetched)
    print("=============================================")

    with open('Links fetched by WebCrawler with Keyphrase.txt', 'w') as f:
        f.write('\n'.join(UniqueLinksFetched))
        f.close()

#=======================================================================
    
WebCrawler("https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher", "concordance")
