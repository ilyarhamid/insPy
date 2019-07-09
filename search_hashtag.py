import time
from post import Post


def get_posts(driver, keyword, max_post=100):
    url = "https://www.instagram.com/explore/tags/%s/" % keyword
    driver.get(url)
    link_list = []
    while True:
        ls = driver.find_elements_by_xpath(xpath="//div[contains(@class,'v1Nh3')]/a")
        driver.execute_script("arguments[0].scrollIntoView();", ls[-1])
        time.sleep(0.5)
        for ele in ls:
            try:
                link = ele.get_attribute("href")
                if link not in link_list:
                    link_list.append(link)
            except:
                pass
        if len(link_list) > max_post:
            break
    post_list = []
    for l in link_list:
        post_list.append(Post(url=l))

    return post_list
