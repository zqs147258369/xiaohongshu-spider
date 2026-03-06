from  DrissionPage  import ChromiumPage
dp= ChromiumPage()

dp.get('https://item.jd.com/10082713763761.html')
dp.ele('css:.all-btn').click()
