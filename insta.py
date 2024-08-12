from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import instaloader

from dotenv import find_dotenv, load_dotenv
import os


class Insta:
    def __init__(self):
        load_dotenv(find_dotenv(".env"))

        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.uname = os.getenv("UNAME")

        browser = input(
            "What is the browser you are using....\ninput, \n'c' for chrome,\n'f' for firefox,\n'e' for Edge,\n's' for Safari,\n").lower()

        site = f"https://www.instagram.com/"

        if browser == "c":
            self.driver = webdriver.Chrome()
        elif browser == "f":
            self.driver = webdriver.Firefox()
        elif browser == "e":
            self.driver = webdriver.Edge()
        elif browser == "s":
            self.driver = webdriver.Safari()
        else:
            self.driver = webdriver.Chrome()

        self.driver.get(site)

        self.wait = WebDriverWait(self.driver, 20)

    def login(self):

        print("Preparing for login...")
        mail = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        mail.send_keys(self.email)

        ps = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        ps.send_keys(self.password)

        button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "._acap")))
        button.click()

        not_now = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1i10hfl")))
        not_now.click()

        notifications = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")))
        notifications.click()
        print("Logged in")

    def make_following_list(self):
        print("Making your following profiles list")
        l = instaloader.Instaloader()
        l.login(user=self.uname, passwd=self.password)

        profile = instaloader.Profile.from_username(l.context, "thamod_the_oxytann")
        following_list = [f.username for f in profile.get_followees()]
        print("following profiles list has been created")
        return following_list

    def unfollowing(self, following_list):
        unfollowing = []
        for index, value in enumerate(following_list):
            print(f"checking user {index + 1}) {value}.....")
            site = f"https://www.instagram.com/{value}"
            self.driver.get(site)

            try:
                following = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "li.xl565be")))[2].find_elements(
                    By.CSS_SELECTOR, "div a span")[0]
                following.click()

                user_following_list = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div.x1dm5mii")))

                users = user_following_list[0]
                user = users.find_elements(By.CSS_SELECTOR, "div div div div")[1].find_elements(By.CSS_SELECTOR,
                                                                                                "div div div div div a div div span")[
                    0].text
                if not self.uname == user:
                    unfollowing.append(value)
            except IndexError:
                unfollowing.append(value)
        self.driver.close()
        return unfollowing

    def unfollow(self, user_lis):
        for index, value in enumerate(user_lis):
            print(f"unfollowing user {index + 1}) {value}.....")
            site = f"https://www.instagram.com/{value}"
            self.driver.get(site)
            foll = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "._acan")))
            foll.click()

            unfoll = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div.x1i10hfl:nth-child(8)")))[0]
            unfoll.click()

        self.driver.close()
