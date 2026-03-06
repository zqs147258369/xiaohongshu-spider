from DrissionPage import ChromiumPage, ChromiumOptions
import os
import re
import requests
import time
import random
# dp=ChromiumPage()
def init_folders():
#  “”“初始化文件夹，确保图片保存目录存在”“”
    if not os.path.exists('img'):
        os.makedirs('img')
        print(' 图片保存文件夹已创建')
def get_search_notes (dp, keyword):
    # “”“获取搜索结果的笔记列表”“”
    # 构造搜索URL（关键词建议URL编码，避免特殊字符问题）
    search_url = f'https://www.xiaohongshu.com/search_result?keyword={keyword}&source=unknown&type=51'
# 启动接口监听（监听搜索接口返回的数据）
    dp.listen.start('search/notes')

    # 访问搜索页面并等待加载
    dp.get(search_url)
    print("🔍 正在加载搜索结果页面...")

    # 等待笔记列表元素显示（超时10秒，确保页面加载完成）
    try:
        dp.wait.ele_displayed('//div[@class="note-item"]', timeout=10)
        print("✅ 搜索结果页面加载完成")
    except TimeoutError:
        print("❌ 页面加载超时，可能原因：1.需要登录 2.网络问题 3.反爬拦截")
        return []

    # 获取接口返回的JSON数据
    r = dp.listen.wait()
    json_data = r.response.body
    items = json_data.get('data', {}).get('items', [])

    print(f"📝 共获取到 {len(items)} 条笔记")
    return items
def download_note_images(dp, item):
#  “”“下载单条笔记的图片”“”
    ids = item.get('id')
    token = item.get('xsec_token')
# 跳过无token的笔记（无法访问详情页）
    if not token:
        print(f"⚠️ 笔记 {ids} 无xsec_token,跳过")
        return

# 构造详情页URL（带token才能访问完整内容）
    detail_url = (
        f'https://www.xiaohongshu.com/explore/{ids}'
        f'?xsec_token={token}&xsec_source=pc_search&source=unknown'
    )

# 访问详情页
    dp.get(detail_url)
    response = dp.html  # 获取页面HTML源码

    # 提取标题（兼容name/property两种属性写法，避免匹配失败）
    title_match = re.findall(r'<meta (?:name|property)="og:title" content="(.*?)"', response)
    old_title = title_match[0] if title_match else f"无标题_{ids}"

    # 清理标题中的非法字符（避免文件保存失败）
    title = re.sub(r'[\\/:*?"<>|]', '_', old_title)

    # 提取图片URL列表
    img_list = re.findall(r'<meta (?:name|property)="og:image" content="(.*?)"', response)
    if not img_list:
        print(f"⚠️ 笔记 {title} 无图片，跳过") 
        return  

# 初始化请求头（固定标准UA，避免版本兼容问题）
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'referer': 'https://www.xiaohongshu.com/',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'cookie':'abRequestId=99462329-4fef-557d-ac19-60b8a98e29fe; a1=19bb188b5d3c95wyhgudp085xvuqyzk546k9p257050000386023; webId=776677fd06f92659984c91f782bee8df; gid=yjDDyYYDYd4fyjDDyYYD2KJ2fqSj2Evxk7fUTW88Y2Ch7j28AvuT2U888qYK8Jq88SjfWiSY; webBuild=5.7.0; acw_tc=0a4a115917688290453212578e305c4105140e50edc1ce8afe8bb3f5fefc0a; web_session=040069b2b25f09ca09f6a0785b3b4b9d65e53e; id_token=VjEAANwhKyUFVmqZeORh+ui1YKxIeeWHLEju4t+/l210htaw/pVv+PaT+Cnb34l+mJL1IOy9IDAT0pK6ImtGjyhw6nOj31eCjJ17oyPC4XtftUVJ5gopJh9WuMWk0ShwLf07asRp; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; customer-sso-sid=68c517597064030231363587f4miutmmwsheohpj; x-user-id-creator.xiaohongshu.com=63c61c4100000000260059a0; customerClientId=010460826135856; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517597064030231347203206qk2lytqtlfnmt; galaxy_creator_session_id=WodbdmQ0Cs3qSYfvGxVFn4ZOCZxHysEMDzHb; galaxy.creator.beaker.session.id=1768829308756050707983; unread={%22ub%22:%22696a248d000000001a01c88a%22%2C%22ue%22:%22696cffc9000000002102b6b3%22%2C%22uc%22:30}; xsecappid=xhs-pc-web; sec_poison_id=74a71961-5acd-40d9-97e2-ce3c19ef16c0; loadts=1768829589750'
    }


# 下载图片
    num = 1
    for img_url in img_list:
        try:
            # 每次请求前更新最新Cookie（关键：保证登录状态有效）
            # cookies = dp.cookies()
            # headers['cookie'] = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            # cookies = dp.cookies()
            # cookie_dict = {cookie.name: cookie.value for cookie in cookies}  # 转字典
            # headers['cookie'] = '; '.join([f'{k}={v}' for k, v in cookie_dict.items()])
            # 获取Cookie列表
            # cookies = dp.cookies()
            # # 遍历每个Cookie对象，提取name和value
            # cookie_str = '; '.join([f'{cookie.name}={cookie.value}' for cookie in cookies])
            # headers['cookie'] = cookie_str
            cookies = dp.cookies()
            cookie_dict = {}
            # 先判断是字典列表还是cookie对象列表
            if cookies and isinstance(cookies[0], dict):
                # 新版：直接取字典的key/value
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            else:
                # 旧版：取cookie对象的name/value属性
                cookie_dict = {cookie.name: cookie.value for cookie in cookies}
            
            # 请求图片（添加超时，避免卡死）
            img_response = requests.get(img_url, headers=headers, timeout=10)
            img_response.raise_for_status()  # 检查请求是否成功（4xx/5xx会抛出异常）
            
            # 保存图片到本地
            img_path = f'img/{title}-{num}.jpg'
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ 图片保存成功：{img_path}")
            num += 1
            
        except Exception as e:
            print(f"❌ 图片 {img_url} 下载失败：{str(e)}")
            continue
def main():
#  “”“主函数：程序入口”“”
# 初始化图片文件夹
    init_folders()
# 配置浏览器选项（适配DrissionPage 4.x版本）
co = ChromiumOptions()
co.set_user_data_path('./xiaohongshu_data')  # 保存登录数据，避免重复登录
co.headless(False)  # 保持浏览器可见，方便手动登录

# 初始化浏览器（传入配置项）
dp = ChromiumPage(co)

# 替换成你要搜索的关键词（示例：羽绒服穿搭，可自行修改）
keyword = "羽绒服穿搭"

try:
    # 获取搜索结果的笔记列表
    items = get_search_notes(dp, keyword)
    
    # 遍历处理每条笔记
    for idx, item in enumerate(items):
        print(f"\n===== 处理第 {idx+1}/{len(items)} 条笔记 =====")
        try:
            download_note_images(dp, item)
            # 关键：笔记之间添加随机延迟，模拟真人操作，降低反爬风险
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"❌ 处理笔记失败：{str(e)}")
            continue
           
except Exception as e:
    print(f"\n❌ 程序运行出错：{str(e)}")
finally:
    # 无论是否出错，最后都关闭浏览器
    dp.quit()
    print("\n👋 程序结束，浏览器已关闭")
if __name__ == "__main__":           
            main()

