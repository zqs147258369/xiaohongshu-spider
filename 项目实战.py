# import requests
# from  bs4   import  BeautifulSoup

# import json

# import  pandas

# url='https://yiqifu.baidu.com/g/aqc/joblist/getDataAjax?q=python&page=1&district=440000&salaryrange='

# headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
#          "referer":"https://yiqifu.baidu.com/g/aqc/joblist?q=python"
# }

# res = requests.get(url=url,headers=headers)
# data =  json.loads(res.text)
# data_list = data["data"]["list"]
# # print(data_list)

# list=[]
# for  i  in data_list:
#     dict = {}
#     dict["城市"] = i['city']
#     dict["公司"] = i['company']
#     dict["学历"] = i['edu']
#     dict["经验"] = i['exp']
#     dict["薪资"]  =  i['salary']
#     bid = i["bid"]
#     jobId = i["jobId"]
#     # print(bid)
#     # print(jobId)

#     detail_url=f"https://yiqifu.baidu.com/g/aqc/jobDetail?bid={bid}&jobId={jobId}"
#     data_res = requests.get(url = detail_url,headers=headers)
#     soup= BeautifulSoup(data_res.text,"html.parser")
#     scrapts = soup.find_all("scrapt")
#     print(scrapts)
#     for s  in scrapts:
#         if  "window.pageData"  in  s.text:
#             text=s.text
#             start=text.find("window.pageData = ")+len("window.pageData = ")

#             end=text.find("|| {}")
#             td = text[start:end]
#             # print(td)
#             detail_res = json.loads(td)
#             dict['岗位职责']  =  detail_res["desc"]
#     list.append(dict)
# print(list)


# pd=pandas.DataFrame(list)

# pd.to_excel("job1.xlsx",index=False)       















