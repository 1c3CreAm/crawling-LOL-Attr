'''
目标：从英雄联盟美服官网获取各个英雄具体的属性值,并把文件储存在目标文件夹内
路线：requests-bs4-re
步骤：
（1）：从"http://lol.duowan.com/hero/"中获取当前已有英雄的名称列表
（2）：http://gameinfo.na.leagueoflegends.com/en/game-info/champions/ + aatrox获取英雄的页面，并得到具体的数值信息
'''

import requests
import re
from bs4 import  BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def getHeroName(namelist,url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,'html.parser')
    aa = soup.find_all('a',target="_blank")
    for i in aa:
        try:
            href = i.attrs['href']
            bb = re.findall(r'\/[a-zA-Z]+\/', href)
            namelist.append(str(bb).split('/')[1])
        except:
            return ''

def getHeroAttr(namelist,url,fliepath):
    count = 0
    for heroname in namelist:
        count = count + 1
        urla = url + heroname + '/'
        html = getHTMLText(urla)
        f = open(fliepath, "a", encoding='utf-8')
        uname =  '-------------------------------------------------------\n'+ heroname + '\n'
        f.write(uname)
        try:
            if html == '':
                f.write('数据暂无')
                continue
            f.close()
            attrinfo = {}
            xinxi = re.findall(r'stat\-label[\s\S]+?\<\/p', html)
            for i in range(len(xinxi)):
                name = xinxi[i].split('\n')[1]
                value = xinxi[i].split('\n')[4]
                attrinfo.update({'属性名称': name.lstrip(), '数值': value.lstrip()})
                with open(fliepath, 'a', encoding='utf-8') as f:
                    f.write(str(attrinfo) + '\n')
            print("\r当前进度: {:.2f}%".format(count * 100 / len(namelist)), end="")

        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(namelist)), end="")
            continue

def main():
    listurl = "http://lol.duowan.com/hero/"
    Attrurl = "http://gameinfo.na.leagueoflegends.com/en/game-info/champions/"
    path = "D:/HeroAttr.txt"
    nameinfo = []
    getHeroName(nameinfo,listurl)
    getHeroAttr(nameinfo,Attrurl,path)

main()
