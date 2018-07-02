#coding utf-8
#using Python3(need urllib), python2 needs urlib and urllib2

import urllib.request
import urllib.error
from urllib.request import ProxyHandler
from urllib.request import build_opener


def useHeader():
    try:
        #using header to simulate browser
#         headers = {}
#         headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        headers = {'User-Agent': "User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        req = urllib.request.Request("https://segmentfault.com/a/1190000012681700", headers=headers)
        html = urllib.request.urlopen(req)
        result = html.read().decode('utf-8')
        print(result)

    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print("error reason: " + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print("error reason: " + str(e.code))
    else:
        print("Succeeded")
        
    return

def useProxy():
    try:
        #using header to simulate browser
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        req = urllib.request.Request("http://fol.zte.com.cn", headers=headers)
        
        proxyAddress={}
        proxyAddress['http'] = "proxyxa.zte.com.cn:80"
        proxyHandler = ProxyHandler(proxyAddress)
        opener = build_opener(proxyHandler)
        
        html = opener.open(req)
        result = html.read().decode('utf-8')
        print(result)

    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print("error reason: " + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print("error reason: " + str(e.code))
    else:
        print("Succeeded")
        
    return

# to be finished
def downloadVideo():
    urllib.request.urlretrieve("https://www.youtube.com/watch?v=FmpDIaiMIeA","kevindownload.mp4")
    print("finished downloading")

def main():
#     response = urllib.request.urlopen("https://segmentfault.com/a/1190000012681700")
#     html = response.read().decode('utf-8')
#     print(html)

#     useHeader()
#     useProxy()

    downloadVideo()    

if __name__ == "__main__":
    main()