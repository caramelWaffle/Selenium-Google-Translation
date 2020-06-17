from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import ElementNotInteractableException

import pandas as pd
from tqdm import tqdm
import time
import os


browser = webdriver.Chrome(executable_path='/Users/macintoshhd/Documents/translate/driver/chromedriver')

df = pd.read_csv("/Users/macintoshhd/Documents/translate/trtpbs-test.csv", encoding="utf-8")
# translated_df = pd.read_csv("/Users/macintoshhd/Documents/translate/eng_test.csv", encoding='utf-8')
# translated_url_list = list(translated_df['url'])

temp_text = ''
for index, row in tqdm(df.iterrows(), total=df.shape[0]):

    # if row['url'] in translated_url_list:
    #     continue

    time.sleep(2)
    text = row['summary']
    browser.get(f'https://translate.google.com/#view=home&op=translate&sl=th&tl=en&text={text}')

    output_ = browser.find_element(By.CLASS_NAME, 'tlid-translation')
    translate = output_.text

    if translate == temp_text:
        browser.refresh()

    output_df = pd.DataFrame()
    output_df.loc[index, 'eng_sum'] = translate
    output_df.loc[index, 'url'] = row['url']

    subdirectory = '/Users/macintoshhd/Documents/translate'
    output_name = os.path.join(subdirectory, 'eng_test.csv')

    if not os.path.isfile(output_name):
        output_df.to_csv(output_name, index=False, encoding='utf-8-sig', header=["eng_sum", "url"])
    else:# else it exists so append without writing the header
        output_df.to_csv(output_name, index=False, encoding='utf-8-sig', mode='a', header=False)
    temp_text = translate
    
if __name__ == '__main__':
    pass