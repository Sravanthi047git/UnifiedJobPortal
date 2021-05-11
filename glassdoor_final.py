import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from load_to_db import db_insert


def scrape_glassdoor(pos, loc, no_of_jobs):
    # set up the driver for extraction
    driver = webdriver.Chrome(executable_path='/Users/twinklem/Desktop/OneDrive/CCA/projects/asp/chromedriver')
    driver.maximize_window()
    driver.get('https://www.glassdoor.co.in/index.htm')
    time.sleep(3)
    # driver.find_element_by_class_name('locked-home-sign-in').click()
    login = driver.find_element_by_css_selector(
        '#SiteNav > nav > div.d-lg-none.d-flex.align-items-center.justify-content-between.px-std.py-xsm.px-md-lg.py-md-std.LockedHomeHeaderStyles__bottomBorder.LockedHomeHeaderStyles__fullWidth > div.d-flex.justify-content-center.order-1.order-md-2.LockedHomeHeaderStyles__flexibleContainer > button')
    driver.execute_script('arguments[0].click();', login)

    div = driver.find_elements_by_css_selector('div.fullContent')
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', div)
    user = driver.find_element_by_xpath('//input[@id="userEmail"]')
    user.send_keys('infidel09@protonmail.com')
    passw = driver.find_element_by_xpath('//input[@id="userPassword"]')
    passw.send_keys('boinkboink')
    button = driver.find_element_by_xpath(
        '/html/body/div[8]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/form/div[3]/div[1]/button').click()

    time.sleep(3)

    search = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="sc.keyword"]')))
    search.send_keys(f'{pos}')
    location = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="sc.location"]')))
    location.send_keys(Keys.COMMAND + "a");
    location.send_keys(Keys.DELETE);
    location.send_keys(f'{loc}')
    time.sleep(2)
    suggestion = driver.find_element_by_css_selector('div.autocomplete-suggestions ')
    driver.execute_script("arguments[0].click();", suggestion);
    driver.find_element_by_xpath('//button[@type="submit"]').click()

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@alt="Close"]'))).click()
    except:
        pass
    time.sleep(3)

    # defining a list to write the data into
    jobs_list = list()

    dates_list = []
    dates = driver.find_elements_by_xpath('//div[@data-test="job-age"]')
    for date in dates:
        dates_list.append(date.text)
    jobs_links = driver.find_elements_by_xpath('//a[@class="jobLink css-1rd3saf eigr9kq2"]')
    parent_window = driver.current_window_handle
    i = 0

    for job in jobs_links:
        i = i + 1
        try:
            driver.execute_script('window.open(arguments[0]);', job)
            all_windows = driver.window_handles
            child_window = [window for window in all_windows if window != parent_window][0]
            driver.switch_to.window(child_window)
            time.sleep(5)
            job_url = driver.current_url
            title = driver.find_element_by_css_selector('div.css-17x2pwl.e11nt52q6').text
            com = driver.find_element_by_css_selector('div.css-16nw49e.e11nt52q1').text
            co = com.split('\n')
            company = co[0]
            location = driver.find_element_by_css_selector('div.css-1v5elnn.e11nt52q2').text
            driver.find_element_by_css_selector('div.css-t3xrds.ecgq1xb2').click()
            time.sleep(2)
            job_desc = driver.find_element_by_xpath('//div[@id="JobDescriptionContainer"]').text

            dict1 = {
                "portal": "Glassdor",
                "title": title,
                "company": company,
                "location": location,
                #"description": job_desc,
                "posteddate": dates_list[i],
                "url": job_url
            }

            jobs_list.append(dict1)

        except:
            pass

        # if i == 2:
 #       if i == no_of_jobs:
 #           driver.quit()
 #           print("Uploading data into the database")
 #           db_insert(jobs_list)
 #           break

        driver.close()
        driver.switch_to.window(parent_window)

    driver.quit()
    print("Uploading data into the database")
    db_insert(jobs_list)