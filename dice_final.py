import time

from selenium import webdriver

from load_to_db import db_insert


def scrape_dice(pos, loc, no_of_jobs):
    # set up the driver for extraction
    driver = webdriver.Chrome(executable_path='/Users/twinklem/Desktop/OneDrive/CCA/projects/asp/chromedriver')
    driver.maximize_window()
    driver.get('https://www.dice.com')  # Enter URL here
    time.sleep(3)
    search = driver.find_element_by_xpath('//input[@placeholder="Job title, skills or company"]')
    search.send_keys(pos)
    location = driver.find_element_by_xpath('//input[@placeholder="Location (zip, city, state)"]')
    location.send_keys(loc)
    button = driver.find_element_by_id('submitSearch-button').click()
    time.sleep(5)

    driver.find_element_by_xpath('//li[@class="pagination-next page-item ng-star-inserted"]//a').click()
    time.sleep(5)
    links = driver.find_elements_by_xpath('//h5/a')
    parent_window = driver.current_window_handle

    # defining a list to write the data into
    jobs_list = list()

    i = 0
    for link in links:
        i = i + 1
        try:
            driver.execute_script('window.open(arguments[0]);', link)
            all_windows = driver.window_handles
            child_window = [window for window in all_windows if window != parent_window][0]
            driver.switch_to.window(child_window)
            time.sleep(8)
            job_title = driver.find_element_by_class_name('jobTitle').text
            company = driver.find_element_by_id('hiringOrganizationName').text
            location = driver.find_element_by_class_name('location').text
            post_time = driver.find_element_by_class_name('posted').text
            job_desc = driver.find_element_by_id('jobdescSec').text
            link_p = driver.current_url
            dict1 = {
                "portal": "Dice",
                "title": job_title,
                "company": company,
                "location": location,
                #"description": job_desc,
                "posteddate": post_time,
                "url": link_p
            }

            jobs_list.append(dict1)

        except:
            pass

        #if i == no_of_jobs:

        break


        driver.close()
        driver.switch_to.window(parent_window)

    driver.quit()
    print("Uploading data into the database")
    db_insert(jobs_list)
