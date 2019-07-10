import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class User:
    def __init__(self, name):
        self.name = name

    def status(self,driver):
        status_dictionary = {'Follow': False, 'Follow Back': False, 'Following': True,
                            'Requested': True}
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            driver.get(url)
        button = driver.find_element_by_class_name("BY3EC")
        txt = ' '.join(button.text.split())
        return status_dictionary[txt]

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

    def get_followers(self, driver, max_followers):
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

    def get_following(self, driver, max_followings):
        url = "https://www.instagram.com/%s/" % self.name
        if driver.current_url != url:
            print("page refreshed!")
            print(driver.current_url, url)
            driver.get(url)
        time.sleep(0.5)
        followings_button = driver.find_elements_by_class_name("-nal3")[2]
        followings_button.click()
        time.sleep(1.0)
        n_prev = -1
        while True:
            ls = driver.find_elements_by_xpath("//div[@class='PZuss']//li")
            if len(ls) == n_prev:
                driver.find_element_by_class_name("dCJp8").click()
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
        pass

    @staticmethod
    def read_from_file(file_path):
        ifl = open(file_path, 'r')
        account_name, password, name = ifl.readline().split()
        return OwnAccount(name, account_name, password)
