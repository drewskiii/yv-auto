# download chromedriver and add to PATH
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()


class YVAutomation:

    URL = "https://my.bible.com/sign-in"

    def __init__(self):
        load_dotenv()
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get(self.URL)
        main_page = self.driver.current_window_handle
        elem = self.driver.find_element_by_id("facebookSigninButton")  # will need to adjust for different sign ins
        elem.click()
        for page in self.driver.window_handles:
            if page != main_page:
                login_page = page
                break
        self.driver.switch_to.window(login_page)
        email_elem = self.driver.find_element_by_id('email')
        email_elem.clear()
        email_elem.send_keys(os.environ.get("EMAIL"))
        pw_elem = self.driver.find_element_by_id('pass')
        pw_elem.clear()
        pw_elem.send_keys(os.environ.get("PW"))  # need to error check
        pw_elem.send_keys(Keys.RETURN)
        self.driver.switch_to.window(main_page)

    def verify_main_page(self):
        like_button_selector = "#current-ui-view > div > div > div.ng-scope > div.moment.moment-vod"
        test = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, like_button_selector))
        )

    def get_plans(self, posts):
        while True:
            last_post = posts[-1]
            last_time = last_post.find_element_by_css_selector('div.moment-top > div.moment-ago').text
            if last_time:
                if "day" in last_time:
                    break
                else:
                    load_more = self.driver.find_element_by_css_selector('#current-ui-view > div > div > button')
                    self.driver.execute_script("arguments[0].click();", load_more)
                    time.sleep(3)
                    main_post = self.driver.find_element_by_css_selector("#current-ui-view > div")
                    posts = main_post.find_elements_by_css_selector("div > div.ng-scope > div.moment.moment-vod")
            else:
                posts.pop()
        return posts

    def like_plans(self, plans):
        for plan in plans:
            post_time = plan.find_element_by_css_selector('div.moment-top > div.moment-ago').text
            if post_time:
                if "day" in post_time:
                    break
            title = plan.find_element_by_css_selector('div.moment-top > div.moment-divider').text
            if "completed" in title and "You" not in title:
                like = plan.find_element_by_css_selector('div.moment-bottom > div.moment-actions > a')
                self.driver.execute_script("arguments[0].click();", like)

    def run(self):
        self.login()
        self.verify_main_page()
        main_post = self.driver.find_element_by_css_selector("#current-ui-view > div")
        posts = main_post.find_elements_by_css_selector("div > div.ng-scope > div.moment.moment-vod")
        plans = self.get_plans(posts)
        self.like_plans(plans)

    def quit(self):
        self.driver.quit()


def main():
    script = YVAutomation()
    script.run()
    script.quit()


if __name__ == "__main__":
    main()
