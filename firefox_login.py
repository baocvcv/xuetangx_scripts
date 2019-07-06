from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import sys
import time
import config

""" parse answers """
lines = open("keys.txt").readlines()
keys = []
units = -1
for line in lines:
    line = line.strip()
    if line == "":
        continue
    elif "Unit" in line or "Final" in line:
        keys.append([])
        units += 1
    elif '.' in line:
        ans = line.split('.')[1].replace(' ', '')
        keys[units].append(ans)
# print(keys)

fp = webdriver.FirefoxProfile()
fp.set_preference("http.response.timeout", 2)
fp.set_preference("dom.max_script_run_time", 2)

driver = webdriver.Firefox(firefox_profile=fp)
actions = ActionChains(driver)
driver.implicitly_wait(2)

driver.get("http://www.xuetangx.com/")

loginBtn = driver.find_element_by_id("header_login")
loginBtn.send_keys(Keys.ENTER)
username = driver.find_element_by_name("username")
username.send_keys(config.username)
passwd = driver.find_element_by_name("password")
passwd.send_keys(config.password)
driver.find_element_by_id("loginSubmit").send_keys(Keys.ENTER)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@id='header_container_avatar']/a[1]"))
)
div1 = driver.find_element_by_xpath("//div[@id='header_container_avatar']/a[1]").send_keys(Keys.ENTER)

""" at dashboard """
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.ID, "otherCourse"))
)
driver.find_element_by_xpath("//div[@id='otherCourse']/div[1]/div[1]/ul[1]/li[1]/a[1]").send_keys(Keys.ENTER)

""" at courseware page """
# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.XPATH, "//section[@id='course-content']/p[1]/a[1]"))
# )

# ele = driver.find_element_by_xpath("//section[@id='course-content']/p[1]/a[1]")
# ele.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='chapter']/h3/a"))
)
for unit in range(config.chapter_start,len(keys)):
    for section in range(len(keys[unit])):
        chapter = driver.find_elements_by_class_name("chapter")[unit]
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='chapter']/h3/a"))
        )
        chapter.find_element_by_xpath("./h3/a").send_keys(Keys.ENTER)
        time.sleep(0.1)

        sect = chapter.find_elements_by_class_name("graded")[section]
        print(sect.find_element_by_xpath("./a/p").text)
        sect.find_element_by_xpath("./a").send_keys(Keys.ENTER)

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, "choicegroup"))
        # )
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//div[@class='chapter']/h3/a"))
        # )
        time.sleep(2)
        problems = driver.find_elements_by_class_name("choicegroup")
        print(len(problems), ' ', len(keys[unit][section]))
        while len(problems) != len(keys[unit][section]):
            time.sleep(0.5)
            problems = driver.find_elements_by_class_name("choicegroup")
            print(len(problems), ' ', len(keys[unit][section]))
        
        for q in range(len(problems)):
            choices = problems[q].find_elements_by_css_selector("input[type='radio']")
            ans = ord(keys[unit][section][q])-ord('A')
            time.sleep(0.1)
            choices[ans].click()
            # for i in range(len(choices)):
            #     if i == ans:
            #         driver.execute_script("arguments[0].setAttribute('checked', 'true')", choices[i])
            #     else:
            #         driver.execute_script("arguments[0].setAttribute('checked', 'false')", choices[i])
            # for i in range(len(choices)):
            #     print(choices[i].text)
            # print(choices[ord(keys[unit][section][q])-ord('A')].text)

        # saveBtn = driver.find_elements_by_class_name('save')
        saveBtn = driver.find_elements_by_class_name('check')
        if len(saveBtn) == 0:
            continue
        saveBtn[0].send_keys(Keys.ENTER)





# unit = 0
# for chapter in driver.find_elements_by_class_name("chapter"): 
#     """ for each chapter """
#     # chapter.find_element_by_xpath("./h3[1]").click()
#     print(chapter.find_element_by_xpath("./h3[1]/a[1]").text)
#     chapter.find_element_by_xpath("./h3[1]/a[1]").click()

#     # WebDriverWait(driver, 10).until(
#     #     EC.element_to_be_clickable((By.XPATH, "//li[@class='graded']/a"))
#     # )
#     sect = 0
#     for section in chapter.find_elements_by_class_name("graded"): 
#         # saveBtn = driver.find_elements_by_class_name('save')
#         # if len(saveBtn) == 0:
#         #     continue
#         # WebDriverWait(driver, 10).until(
#         #     EC.element_to_be_clickable(saveBtn[0])
#         # )

#         """ for each section """
#         print(section.find_element_by_xpath("./a/p").text)
#         # section.find_element_by_xpath("./a").send_keys(Keys.ENTER)
#         link = section.find_element_by_xpath("./a") # send_keys(Keys.CONTROL + 't')
#         actions.context_click(link).perform()
#         actions.send_keys(Keys.ARROW_DOWN).perform()
#         actions.send_keys(Keys.ENTER).perform()


#         problems = driver.find_element_by_class_name("problem")
#         ans_str = keys[unit][sect]
#         question = 0
#         for problem in problems.find_elements_by_css_selector('span'):
#             choices = problem.find_elements_by_css_selector("input[type='radio']")
#             print(len(choices), ' ', ord(ans_str[question])-ord('A'))
#             # choices[ord(ans_str[question]) - ord('A')].click()
#             question += 1

#         saveBtn.click()
#         sect += 1
#     unit += 1
