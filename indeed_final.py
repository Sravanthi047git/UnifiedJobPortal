import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from load_to_db import db_insert


def scrape_indeed(pos, loc, no_of_jobs):
    # set up the driver for extraction
    driver = webdriver.Chrome(executable_path='/Users/twinklem/Desktop/OneDrive/CCA/projects/asp/chromedriver')
    driver.maximize_window()
    # driver.get('https://www.indeed.com/jobs?q=Software+Tester&l=New+York')

    # print ('https://www.indeed.com/jobs?q=' +  pos + '&l=' + loc)
    driver.get('https://www.indeed.com/jobs?q=' + pos + '&l=' + loc)

    # defining a list to write the data into
    jobs_list = list()

    parent_window = driver.current_window_handle
    titles = driver.find_elements_by_tag_name('h2')

    i = 0
    for title in titles:

        i = i + 1
        link = title.find_element_by_tag_name('a')
        link_p = link.get_attribute('href')
        driver.execute_script('window.open(arguments[0]);', link)
        all_windows = driver.window_handles
        child_window = [window for window in all_windows if window != parent_window][0]
        driver.switch_to.window(child_window)
        time.sleep(5)

        try:
            job_desc = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="jobDescriptionText"]'))).text

            title = driver.find_element_by_tag_name('h1').text

            try:
                company = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]//a'))).text

            except:

                company = driver.find_element_by_xpath('//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]').text
            time.sleep(2)
            try:
                location = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/div[4]/div[1]/div[2]/div/div/div[2]').text
            except:
                location = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/div/div/div[2]').text
            days = driver.find_element_by_css_selector(
                '#viewJobSSRRoot > div.jobsearch-JobComponent.icl-u-xs-mt--sm.jobsearch-JobComponent-bottomDivider > div.jobsearch-JobTab-content > div.jobsearch-JobMetadataFooter > div:nth-child(2)').text

            dict1 = {
                "portal": "Indeed",
                "title": title,
                "company": company,
                "location": location,
                #"description": job_desc,
                "posteddate": days,
                "url": link_p
            }

            jobs_list.append(dict1)

        except:
            pass

#        if i == no_of_jobs:

#            break

        driver.close()
        driver.switch_to.window(parent_window)

    driver.quit()
    print("Uploading data into the database")
    db_insert(jobs_list)