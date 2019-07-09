import time


class Post:
    def __init__(self, url):
        self.url = url

    def like(self, driver):
        if driver.current_url != self.url:
            driver.get(self.url)
        button = driver.find_element_by_class_name("dCJp8")
        button.click()
        return None

    def comment(self, driver, content):
        if driver.current_url != self.url:
            driver.get(self.url)
        block = driver.find_element_by_class_name("Ypffh")
        block.click()
        time.sleep(1.0)
        driver.find_element_by_class_name("Ypffh").send_keys(content + '\n')
        return None

    def number_of_likes(self, driver):
        if driver.current_url != self.url:
            driver.get(self.url)
        likes = driver.find_element_by_class_name("zV_Nj")
        n = likes.text.split()[0]
        return n