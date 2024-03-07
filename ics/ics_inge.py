from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import datetime
import uuid
import dateparser
import time

from CoursInge import course_inge


URL = "https://horaires2023.condorcet.be/invite"

course_dict = {"INGE":course_inge}

WAITING_TIME = 5
output ="BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:adamgibbons/ics\nMETHOD:PUBLISH\nX-PUBLISHED-TTL:PT1H\n"

def move_to_start_position(driver):
    # Go into "Formations" tab
    formation = driver.find_element(By.XPATH, '//div[text()="Promotions"]')
    action = ActionChains(driver)
    action.move_to_element(formation)
    action.click()
    action.perform()

    # Go into "Récapitulatif des cours" tab
    recap = driver.find_element(By.XPATH, '//div[text()="Options"]')
    action = ActionChains(driver)
    action.move_to_element(recap)
    action.move_by_offset(120, 30)
    action.click()
    action.perform()


def move_to_combo(driver):
    select = driver.find_element(By.XPATH, '//div[@class="ocb_cont as-input as-search"]')
    action = ActionChains(driver)
    action.move_to_element(select)
    action.move_by_offset(5, 5)
    action.click()
    action.perform()


def move_to_course(driver,course):
    action = ActionChains(driver)
    action.send_keys(course)
    action.send_keys(Keys.ENTER)
    action.perform()


def get_information(driver, course_id, start=-1, end=-1):
    print(course_id)
    global output
    timeZone = "Europe/Brussels"
    course = course_dict[course_id]
    tables = driver.find_elements(By.XPATH,'//table[@class="as-content"]/tbody/tr')

    if start == -1 or end == -1:
            start, end = 1, len(tables)

    for i in range(start, end,2):
        course_name = tables[i].find_elements(By.XPATH,'./td/table/tbody/tr/td/span')[0].text

        if course_name in course:
            course_name = course[course_name]
        else:
            continue
        list_cursus = tables[i+1].find_elements(By.XPATH,'./td/div/table/tbody/tr')
        for cursus in list_cursus:
            info  = cursus.find_elements(By.XPATH,'./td')

            date  = info[0].find_element(By.XPATH,'./ul/li').get_attribute("innerHTML").replace("&nbsp;", " ")
            _time = info[1].get_attribute("innerHTML").replace("&nbsp;", " ")
            start = dateparser.parse(date + ' ' + _time[3:8]).strftime("%Y-%m-%dT%H:%M:%S")
            end   = dateparser.parse(date + ' ' + _time[10:17]).strftime("%Y-%m-%dT%H:%M:%S")
            start = start.replace(":","").replace("-","")
            end = end.replace(":","").replace("-","")

            teacher = info[3].get_attribute("innerHTML").replace("&nbsp;", " ")
            room = info[4].get_attribute("innerHTML").replace("&nbsp;", " ")
            uid = str(uuid.uuid4())
            today = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
            today = today.replace(":","").replace("-","")

            output += "BEGIN:VEVENT\n"
            output += "DTSTAMP:" + today + "Z\n"
            output += "UID:" + uid + "\n"
            output += "SUMMARY:" + course_name + "\n"
            output += "DTSTART;TZID=" + timeZone + ":" + start + "\n"
            output += "DTEND;TZID=" + timeZone + ":" + end + "\n"
            output += "LOCATION:" + room + " | " + teacher + "\n"
            output += "END:VEVENT\n"



options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
driver.get(URL)
print("start")
time.sleep(WAITING_TIME) # wait for the page to load
move_to_start_position(driver)
move_to_combo(driver)
time.sleep(WAITING_TIME)
move_to_course(driver, "B3-Bac en sciences de l'ingénieur industriel (Charleroi)")
time.sleep(WAITING_TIME)
get_information(driver,"INGE")
time.sleep(WAITING_TIME)
print("end")

output += "END:VCALENDAR"
with open('events/events_inge.ics', 'w') as my_file:
    my_file.writelines(output)