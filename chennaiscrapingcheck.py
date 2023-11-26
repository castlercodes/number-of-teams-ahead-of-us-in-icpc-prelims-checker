import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

chen = 0
tot_unq = 0
tot = 0
encountered_colleges = set()

# Open the website
url = "https://codedrills.io/contests/icpc-india-preliminary-2023/scoreboard"
driver.get(url)

# Wait for the page to load by checking for the presence of the specified class
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-text-field__slot")))

while True:
    table_wrapper = driver.find_element(By.CLASS_NAME, "v-data-table__wrapper")
    table_html = table_wrapper.get_attribute("outerHTML")

    soup = BeautifulSoup(table_html, "html.parser")

    for anchor_tag in soup.find_all("a", class_=["router_link"]):
        href = anchor_tag.get("href")
        if href:
            driver.execute_script(f"window.open('{href}', '_blank');")

            driver.switch_to.window(driver.window_handles[1])

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "col")))

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-v-684389c3]")))
                span = driver.find_element(By.CSS_SELECTOR, "span[data-v-684389c3]")

                print(span.text)

                div_col = driver.find_elements(By.XPATH, "//div[@data-v-684389c3=''][@class='col']")[1]
                college_name = div_col.text

                print(college_name)

                if college_name not in encountered_colleges:
                    print(f"New college encountered: {college_name}")

                    if "amritapuri" in span.text.lower():
                        encountered_colleges.add(college_name)
                        print(f"Substring 'amritapuri' found in the page: {driver.current_url}")
                        chen += 1
                    
                    tot_unq += 1
                tot += 1

                print(chen, tot_unq, tot)

            except Exception as e:
                print(f"Error: {e}")

            finally:
                if driver.window_handles:
                    driver.close()

                    driver.switch_to.window(driver.window_handles[0])
        else:
            print("No 'href' attribute found in the anchor tag.")

    # Scroll down to the bottom of the page
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Click the div with classname "v-data-footer__icons-after"
    try:
        overlay_div = driver.find_element(By.CLASS_NAME, "v-data-footer__icons-after")
        overlay_div.click()

        # Wait for 2 seconds before continuing
        time.sleep(2)

    except Exception as e:
        print(f"Error clicking div: {e}")

# Close the browser
driver.quit()
