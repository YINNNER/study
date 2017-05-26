import requests
import urllib.request
import urllib
import hashlib
from bs4 import BeautifulSoup as bs
import urllib.parse
#from .forms import studentForm, teacherForm


def spider(username, password, yzm_text, yzm_cookie):
    home_url = 'http://210.42.121.241'
    login_url ='http://210.42.121.241/servlet/Login'
    #image_url = 'http://210.42.121.241/servlet/GenImg'
    login_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
    #提交的数据
    data = urllib.parse.urlencode({
        'id': username,
        'pwd': login_pwd,
        'xdvfb': yzm_text,
    })
    data = data.encode(encoding='utf-8')
    #登录请求
    req = urllib.request.Request(login_url, data, headers={'Cookie': yzm_cookie})
    content = urllib.request.urlopen(req).read()
    #网页信息
    soup = bs(content, "lxml")
    namediv = soup.find_all(attrs={'id': 'nameLable'})
    termspan = soup.find_all(attrs={'id': 'term'})

    stu_name = '' #姓名
    stu_term = '' #学期

    for name in namediv:
        stu_name = name.text.encode('utf-8').lstrip().rstrip()
    for term in termspan:
        stu_term = term.text.encode('utf-8').lstrip().rstrip()
    # print("你的名字："+stu_name)
    # print("现在是"+stu_term)
    # print page_url

    #开始爬取课表
    table_url = 'http://210.42.121.241/stu/stu_course_parent.jsp'
    requset = urllib.request.Request(table_url, headers={'Cookie':yzm_cookie})
    class_table = urllib.request.urlopen(requset).read()
    tsoup = bs(class_table, 'lxml')
    page_iframe = tsoup.find_all(attrs={'id': 'iframe0'})
    page_url = home_url  # 课程表所在的url
    for page in page_iframe:
        page_url = page_url + page.get('src')[:-8]+"%CF%C2&state="
    #print(page_url)
    requset = urllib.request.Request(page_url, headers={'Cookie': yzm_cookie})
    #课表的详细内容：table_content
    table_content = urllib.request.urlopen(requset).read()
    get_classes(table_content)

    # print csoup.prettify()
    # # print tsoup.prettify()


#获取课程信息
def get_classes(table_content):
    csoup = bs(table_content, 'lxml')
    listTable = csoup.find_all(attrs={'class': 'table listTable'})
    tr = listTable[0].find_all('tr')
    tr_num = len(tr)
    for i in range(1, tr_num):
        td = tr[i].find_all('td')
        course_num = td[0].text.encode("utf-8").strip() #课头号
        course_name = td[1].text.encode("utf-8").strip() #课程名字
        course_type = td[2].text.encode("utf-8").strip() #课程类型（必修或选修）
        course_college = td[4].text.encode("utf-8").strip() #授课学院
        course_teacher = td[5].text.encode("utf-8").strip() #授课老师
        course_major = td[6].text.encode("utf-8").strip() #专业
        course_point = td[7].text.encode("utf-8").strip() #学分
        course_time = td[9].text.encode("utf-8").strip() #课程时间
        time_dict = course_time.split(b":")
        day =  time_dict[0] #形式为"周一"
        class_num = time_dict[1].split(b";")[1].split(b"--")[0].split(b"-")
        start_num = class_num[0] #开始节数
        end_num = class_num[1] #结束节数
        course_name = course_name.decode("utf-8")
        course_time = course_time.decode('utf-8')
        #print(course_name)
        #done
        #print("第"+str(i)+"门课"+course_name+"时间为"+course_time)
        #print(course_time)
    # print tr[15]
    # td = tr[15].find_all('td')
    # td_num = len(td)
    # print td_num
    # cource_num = tr[15].fin
    #     print(str(i)+tr[i].text.encode("utf-8"))
    # print csoup.prettify()
#spider('2016301500226', hashlib.md5('19980814'.encode('utf-8')).hexdigest())
# if __name__ == "__main__":
#     login_id = '2016301500226'
#     pwdd = '19980814'
#     pwddd = pwdd.encode('utf-8')
#     login_pwd = hashlib.md5(pwddd).hexdigest() # 输入你的密码
#     spider(login_id, login_pwd)


def save_img(username, yzm_image):
    yzm_file = 'file/yzm/'+str(username) + ".jpg"
    with open(yzm_file, 'wb') as f:
        f.write(yzm_image)