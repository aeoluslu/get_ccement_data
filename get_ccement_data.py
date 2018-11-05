import urllib.request  
import urllib  
import gzip  
import http.cookiejar 
import types  
import time
from datetime import datetime, timedelta

def getOpener(head):  
    # deal with the Cookies  <pre name="code" class="python">   
    cj = http.cookiejar.CookieJar()  
    pro = urllib.request.HTTPCookieProcessor(cj)  
    opener = urllib.request.build_opener(pro)  
    header = []  
    for key, value in head.items():  
        elem = (key, value)  
        header.append(elem)  
    opener.addheaders = header  
    return opener  
  
#定義一個方法來解壓返回信息  
def ungzip(data):  
    try:        # 嘗試解壓  
        print('正在解壓.....')  
        data = gzip.decompress(data)  
        print('解壓完畢!')  
    except:  
        print('未經壓縮, 無需解壓')  
    return data  


def data_parser(parser_data,province_name,data_range_week):  
    parser_data=parser_data[parser_data.find('data: [[')+5:parser_data.find('dataGrouping: {')-2]
    parser_data=parser_data[parser_data.find('[[')+2:parser_data.find(']],')]
    data_array=parser_data.split('],[')
    print(len(data_array))
    f = open('D:/test_data/'+time.strftime("%Y-%m-%d")+'_result.csv','a')
    f.write('省份,'+province_name+'\n')
    record_date='日期'
    record_open='本周初价格'
    record_high='本周最高'
    record_low='本周最低'
    record_close='本周末价格'
    i=0
    while i < len(data_array) :
        if datetime.now() - datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(data_array[i].split(',')[0])/1000)), '%Y-%m-%d %H:%M:%S') < timedelta(weeks=data_range_week) :
            record_date= record_date+','+time.strftime("%Y-%m-%d", time.localtime(float(data_array[i].split(',')[0])/1000))
            record_open=record_open+','+data_array[i].split(',')[1]
            record_high=record_high+','+data_array[i].split(',')[2]
            record_low=record_low+','+data_array[i].split(',')[3]
            record_close=record_close+','+data_array[i].split(',')[4]
        i+=1
    f.write(record_date+'\n')
    f.write(record_open+'\n')
    f.write(record_high+'\n')
    f.write(record_low+'\n')
    f.write(record_close+'\n')
    f.close

#def getCementPriceByProvince(ProvinceId):
#    print('省份ID : '+ProvinceId)
#    url = 'https://data.ccement.com/area/price/'+ProvinceId+'.html' #水泥價格 
#    print('Download : '+url)
#    op = opener.open(url)  
#    data = op.read()  
#    data = ungzip(data)  
#    return data

def main():  
    #封裝頭信息，偽裝成瀏覽器  
    global opener
    global op
    header = {  
        'Connection': 'Keep-Alive',  
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',  
        'Accept': 'application/json, text/javascript, */*; q=0.01',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',  
        'Accept-Encoding': 'gzip, deflate',  
        'X-Requested-With': 'XMLHttpRequest',  
        'Host': 'i.ccement.com',  
    }  
  
  
    url = 'http://i.ccement.com/Ajax/loginHandler.ashx?reUrl=http://data.ccement.com/area/price/provincelist.html'  
    opener = getOpener(header)  
    
    id = 'usre'#你的用户名  
    password = 'pwd'#你的密碼  
    postDict = {  
            'act':'',
            'txtUserName': id,  
            'txtMd5Password': password,  
            'checkbox': 'checked',
            'checktype': '', 
    }  
  
    postData = urllib.parse.urlencode(postDict).encode()  
    op = opener.open(url, postData)  
    data = op.read()  
    data = ungzip(data)  
    print(data)

    data_range_week=52 #要抓取的資料週數(由今天往前推幾週)
 ## Open file
    province_data = open('ccement_list.csv', "r")
    lines = province_data.readlines()
    province_data.close()
    for i in range(len(lines)):
        Provincename=lines[i].split(',')[0]
        ProvinceId=lines[i].split(',')[1].strip('\n')
        print ('Provincename :'+Provincename)
        print ('ProvinceId :'+ProvinceId)
        #ProvinceId='410000'
        #print('省份ID : '+ProvinceId)
        #url = 'https://data.ccement.com/area/price/410000.html' #水泥價格 
        url = 'https://data.ccement.com/area/price/'+ProvinceId+'.html' #水泥價格 
        print('Download URL:'+url)
        op = opener.open(url)  
        data = op.read()  
        data = ungzip(data)  
        #data=getCementPriceByProvince('410000')
        parser_data = data.decode('utf-8')
        #Provincename='河南'
        data_parser(parser_data,Provincename,data_range_week)
        time.sleep(3
        )




    
    opener.close


if __name__ == "__main__":
    main()