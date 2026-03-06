#我们第一次请求唯品会的数据信息（没有带参数）

#导入request
import  requests
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
          "referer":"https://category.vip.com/" 
}

url ='https://mapi-pc.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'
params= {
    

}
res= requests.get(url,headers=headers,params=params)

print(res.text)
print(res.status_code)
#{"msg":"client id from request api_key param is Empty!","code":11004,"data":{}