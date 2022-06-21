from selenium import webdriver
import time

if __name__ == "__main__":
    chrome = webdriver.Chrome()
    query_string = "(%23nanjingmassacre)"
    query_url = "https://twitter.com/search?q=%s&src=typed_query&f=live"%query_string
    chrome.get(query_url)
    js = "var q=document.documentElement.scrollTop=1000000000000"
    for i in range(10000000000):
        print(i)
        """
        由于在机械下滑的过程中，可能会由于网络问题或者推特设置的限制导致代码无法进行，因此要模拟上滑动以继续请求，而这个在requests请求中是较为复杂的
        """
        if i % 10 == 0:
            chrome.execute_script("var q=document.documentElement.scrollTop=10")
            print("return to scroll-10")
        chrome.execute_script(js)
        # time.sleep(1)
    print("down")
