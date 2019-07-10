import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from inspy.post import Post

class User:
    def __init__(self, name):
        self.name = name

    def status(self,driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        button = driver.find_element_by_class_name("BY3EC")
        txt = ' '.join(button.text.split())
        return txt

    def follow(self, driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        button = driver.find_element_by_class_name("BY3EC")
        button.click()
        return None

    def unfollow(self, driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        button1 = driver.find_element_by_class_name("BY3EC")
        button1.click()
        time.sleep(0.5)
        button2 = driver.find_element_by_class_name("aOOlW")
        button2.click()
        return None

    def get_info(self, driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        element = driver.find_element_by_class_name("-vDIg")
        return element.text

    def number_of_posts(self, driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        time.sleep(0.5)
        posts = driver.find_elements_by_class_name("-nal3")[0]
        return posts.text.split()[0]

    def get_followers(self, driver, max_followers=100000):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        time.sleep(0.5)
        follower_button = driver.find_elements_by_class_name("-nal3")[1]
        follower_button.click()
        time.sleep(1.0)
        n_prev = -1
        while True:
            ls = driver.find_elements_by_xpath("//li[@class='wo9IH']")
            if len(ls) == n_prev:
                break
            n_prev = len(ls)
            driver.execute_script("arguments[0].scrollIntoView();", ls[-1])
            time.sleep(0.5)
            if len(ls) > max_followers:
                break
        user_list = []
        for ele in ls:
            txt = ele.text
            user_name = txt.split('\n')[0]
            user_list.append(User(user_name))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        return user_list

    def get_following(self, driver, max_followings=100000):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        time.sleep(0.5)
        followings_button = driver.find_elements_by_class_name("-nal3")[2]
        followings_button.click()
        time.sleep(1.0)
        n_prev = -1
        while True:
            ls = driver.find_elements_by_xpath("//div[@class='PZuss']//li")
            if len(ls) == n_prev:
                break
            n_prev = len(ls)
            driver.execute_script("arguments[0].scrollIntoView();", ls[-1])
            time.sleep(0.5)
            if len(ls) > max_followings:
                break
        user_list = []
        for ele in ls:
            txt = ele.text
            user_name = txt.split('\n')[0]
            user_list.append(User(user_name))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        return user_list

    def get_posts(self, driver):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        time.sleep(0.5)
        ls = driver.find_elements_by_xpath(xpath="//div[contains(@class,'v1Nh3')]/a")
        if len(ls) == 0:
            return None
        post_list = []
        for ele in ls:
            link = ele.get_attribute("href")
            post_list.append(Post(link))
        return post_list


class OwnAccount(User):

    def __init__(self, name, account_name, password):
        self.name = name
        self.account_name = account_name
        self.password = password

    def login(self, driver):
        account_name = self.account_name
        password = self.password
        driver.get("https://www.instagram.com/accounts/login")
        time.sleep(1.0)
        input_list = driver.find_elements_by_xpath("//input")
        input_list[0].send_keys(account_name)
        input_list[1].send_keys(password + '\n')
        time.sleep(3.0)
        return None

    def clean_followers(self, driver):
        follower_list = []
        following_list = []
        following_list_obj = self.get_following(driver)
        follower_list_obj = self.get_followers(driver)
        for u in follower_list_obj:
            follower_list.append(u.name)

        for u in following_list_obj:
            following_list.append(u.name)

        unfollow_list = []
        for name in following_list:
            if name not in follower_list:
                unfollow_list.append(name)

        print("%s out of %s accounts didn't follow you back" % (len(unfollow_list), len(following_list)))
        for user in following_list_obj:
            if user.name in unfollow_list:
                user.unfollow(driver)
        return None

    @staticmethod
    def read_from_file(file_path):
        ifl = open(file_path, 'r')
        account_name, password, name = ifl.readline().split()
        return OwnAccount(name, account_name, password)
