import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# 设置浏览器选项
options = Options()
# 限制CSS加载
options.set_preference("permissions.default.stylesheet", 2)
# 限制图片加载
options.set_preference('permissions.default.image', 2)
# 限制JavaScript执行
options.set_preference('javascript.enabled', False)

driver = webdriver.Firefox(options=options) # 启用火狐驱动

driver.get('https://www.icauto.com.cn/weizhang/wzd/310000/') # 模拟浏览器打开网页

# 创建df存储爬取数据
data = pd.DataFrame(columns=['位置','违章指数'])
hrefs = []

for count in range(35):
    # 页面计数
    # 获取监控点位置和违章指数
    ul = driver.find_element(By.CSS_SELECTOR, "html body div.wzcx div.cdz-l div.cdz-ccotent ul")
    li_list = ul.find_elements(By.TAG_NAME, 'li')
    page = driver.find_element(By.CLASS_NAME, 'cdzpages')
    pages = page.find_elements(By.TAG_NAME, 'a')

    for i in range(len(li_list)):
        name_level = li_list[i].text

        # 获取监测点名与违章指数
        s = pd.Series(name_level.split('\n'), index=['位置','违章指数'])
        s['违章指数'] = s['违章指数'].split('：')[1]
        a = li_list[i].find_element(By.TAG_NAME, 'a')

        # 获取超链接
        href = a.get_attribute("href")
        hrefs.append(href)
        data = pd.concat([data, pd.DataFrame(s).T], ignore_index=True)

    pages[-1].click()
    print('当前第{}页'.format(count+1))

print('爬取结束')
data['超链接'] = pd.Series(hrefs)

driver.close()

# 存储为csv
data.to_csv('data/video_surveillance.csv')