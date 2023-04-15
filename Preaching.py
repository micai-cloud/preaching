import requests,re,time
from lxml import html
from sendemil import send
tomTime = time.strftime("%Y-%m-%d",time.localtime(time.time()+86400))
#print(tomTime)
url = 'http://job.ysu.edu.cn/jyxt/sczp/zphgl/cxZprlList.zf'
etree = html.etree
def getxjh(xurl):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
           }

    # print(data)
    response = requests.post(url=xurl, headers=headers)
    # print(response.text)
    tree = etree.HTML(response.text)
    lists1 = tree.xpath('.//div[@class="con-info"]')
    lists2 = tree.xpath('.//div[@class="dwxx-info"]')
    detailedstr = ''
    #print(lists1)
    for i in lists1:
        position = i.xpath('normalize-space(./span[1]/text())')
        present = i.xpath('normalize-space(./span[2]/text())')
        detailedstr += present +'  '+ position +'  '
    for i in lists2:
        types = i.xpath('normalize-space(./span[1]/text())')
        industry = i.xpath('normalize-space(./span[2]/text())')
        Number = i.xpath('normalize-space(./span[3]/text())')
        location = i.xpath('normalize-space(./span[4]/text())')
        #print(types,industry,Number,location)
        detailedstr += types +'  '+ industry+'  '+ Number +'  '+ location
    #print(detailedstr)
    return detailedstr
def req(url,datastr):
    global tablename
    content = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3830.400',
    }
    data = {'rq': datastr}
    response = requests.post(url=url, headers=headers, data=data)
    jobdict = response.json()
    for job in jobdict:
        if job['rq'] == datastr:
            joblist = job['list']
            #print(datastr)
            num = 1
            for i in joblist:
                mc = i['mc']
                joburl = 'http://job.ysu.edu.cn/jyxt/sczp/zphgl/cxZprlXq.zf?id='+i['id']+'&ywlx='+i['ywlx']
                detailedstr = getxjh(joburl)
                if i['ywlx'] == 'xjh':
                    #print(str(num) +'  '+ '现场宣讲会' +'  '+ mc + '  ' +'\n'+ detailedstr +'\n'+ joburl +'\n')
                    content += str(num) +'  '+ '现场宣讲会' +'  '+ mc + '  ' +'\n'+ detailedstr +'\n'+ joburl +'\n\n'
                else:
                    #print(str(num) +'  '+ '空中宣讲会' + '  ' + mc + '  '  + '\n' + detailedstr +'\n' + joburl +'\n')
                    content += str(num) +'  '+ '空中宣讲会' + '  ' + mc + '  '  + '\n' + detailedstr +'\n' + joburl +'\n\n'
                num += 1
            if content != '':
                send(datastr,content)
                #print(content)
            break
req(url=url,datastr=tomTime)
#req(url=url,datastr='2023-04-17')
