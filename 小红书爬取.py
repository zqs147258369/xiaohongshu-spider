import  requests
import  re
import os  # 先导入os模块
import  time
import  random
from  DrissionPage  import  ChromiumPage
# 在请求网页之前，添加创建文件夹的代码
if not os.path.exists('img'):
    os.makedirs('img')  # 自动创建img文件夹（如果不存在）
dp=ChromiumPage()
# # 监听数据包
dp.listen.start('search/notes')
search_url = 'https://www.xiaohongshu.com/search_result?keyword=%E5%85%A5%E5%81%95%E5%A5%BD&source=unknown&type=51'

dp.get(search_url)
dp.wait.ele_displayed('//div[@class="note-item"]', timeout=10)
# dp.wait(3)  # 等待3秒
r= dp.listen.wait()
json_data=r.response.body
# print(json_data)
items= json_data['data']['items']
print(items)
for  item  in  items:
    ids=item['id']
    if '-'  not in  ids:
        token= item['xsec_token']
        print(ids,token)

    cookies = dp.cookies.all()
    headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()])
    }
    url= f'https://www.xiaohongshu.com/explore/{ids}?xsec_token={token}=&xsec_source=pc_search&source=unknown'
    dp.get (url)
    response=dp.html
    try:    
        title_match = re.findall(r'<meta (?:name|property)="og:title" content="(.*?)">', response)
        img_list=re.findall(r'<meta (?:name|property)="og:image" content="(.*?)">', response)
        if title_match:
            old_title = title_match[0]
        else:
            old_title = f"无标题_{ids}"  # 兜底处理
        # 替换特殊字符
        title= re.sub(r'[\\/:*?"<>|]', '_', old_title)  # 清理标题里的非法字符
        # print(title)
        # print(img_list)
        # print(len(img_list))
        num=1
        for  index  in  img_list:
            # 每次请求图片前也更新 Cookie
            cookies = dp.cookies.all()
            headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            img_content = requests.get(index, headers=headers).content
            file_path = os.path.join("img", f"{title}-{num}.jpg")
            with open(file_path, 'wb') as f:
                f.write(img_content)
                num+=1
                time.sleep(random.uniform(1, 3))
        print(index)
        
    except Exception as e:
        print(f"保存图片失败: {e}")
