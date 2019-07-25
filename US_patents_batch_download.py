#爬取美国专利网指定公司的专利
#by---jzx
#2016-11-8
import re
from bs4 import BeautifulSoup
import requests
import os
import time
#存储数据
def store_data(headers, dictionary, search_string):
    dictionary['patent_name'] = dictionary['patent_name'].replace('\n', ' ').replace('"', ' ')[:100]
    folder_name = 'C:\\Users\\223\\Desktop\\ML_learning\\爬虫\\' + search_string + '/' + dictionary['patent_name'] + '(' + dictionary['patent_code'] + ')'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = folder_name + '/data.txt'
    pdfname = folder_name + '/full_pdf.pdf'
    data_list = ['patent_code', 'patent_name', 'year', 'inventor_and_country_data', 'description', 'full_pdf_file_link']
    with open(filename, 'w') as f:
        for data in data_list:
            f.write(data + ': \n' + dictionary[data] + '\n')
    f.close()
    try:
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/'
                          '1.63.6726.400 QQBrowser/10.2.2265.400',
            'Host': 'pimg-fpiw.uspto.gov',
            'Referer': 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1='
                       'Ronds&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT',
            'If-None-Match': 'KQwjMJ050avfdH47mppTfvU3CBA='}  #这边貌似和head没有任何关系
        r = requests.get('http:'+dictionary['full_pdf_file_link'], headers=headers)
        time.sleep(3)
        with open(pdfname, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        fd.close()
    except:
        print('there is something wrong with this patent')
#获取数据
def get_patent_data(url, headers, search_string):
    tmp_s = requests.session()
    try:
        r2 = tmp_s.get(url, headers=headers)
    except:
        print('There is something wrong with this patent')
        return
    text2 = r2.text
    tmp_soup = BeautifulSoup(text2, "html.parser")
    patent_data = dict()
    # print(text2)
    patent_data['patent_code'] = tmp_soup.find('title').next[22:]   #22是因为显示的是'United States Patent: 10175261'，前面的字符是不需要的
    patent_data['patent_name'] = tmp_soup.find('font', size="+1").text[:-1]
    tmp1 = text2[re.search('BUF7=', text2).span()[1]:]
    patent_data['year'] = tmp1[:re.search('\n', tmp1).span()[0]]
    patent_data['inventor_and_country_data'] = tmp_soup.find_all('table', width="100%")[2].contents[1].text
    tmp1 = text2[re.search('Description', text2).span()[1]:]
    tmp2 = tmp1[re.search('<HR>', tmp1).span()[1]:]
    patent_data['description'] = tmp2[re.search('<BR>', tmp2).span()[0]:(re.search('<CENTER>', tmp2).span()[0] - 9)]. \
        replace('<BR><BR> ', '')
    tmp3 = tmp2[:re.search('<TABLE>', tmp2).span()[0]]
    tmp_soup = BeautifulSoup(tmp3, "html.parser")
    pdf_link = tmp_soup.find('a').get('href')
    r3 = tmp_s.get(pdf_link)
    text3 = r3.text
    tmp_soup = BeautifulSoup(text3, "html.parser")
    pdf_file_link = tmp_soup.find('embed').get('src')
    patent_data['pdf_file_link'] = pdf_file_link
    patent_data['full_pdf_file_link'] = pdf_file_link.replace('pdfpiw.uspto.gov/', 'pimg-fpiw.uspto.gov/fdd/'). \
        replace('1.pdf', '0.pdf')
    store_data(headers, patent_data, search_string)
#主函数
def main():
    s = requests.session()
    search_string_1 = 'Ronds'
    search_string_2 = ''
    # keywords = list()
    # while True:
    #     print('what do you want to do?(a: add a key word for searching, q:quit adding words and start)')
    #     command = input('command:')
    #     if command == 'a':
    #         word = input('keyword: ')
    #         if word not in keywords:
    #             keywords.append(word)
    #     elif command == 'q':
    #         break
    #     else:
    #         print('please input a valid command')
    # if len(keywords) == 0:
    #     return
    # search_string = ''
    # for keyword in keywords:
    #     search_string += keyword
    #     search_string += '+'
    # search_string = search_string[:-1]
    main_folder_name = 'C:\\Users\\223\\Desktop\\ML_learning\\爬虫\\' + search_string_1
    if not os.path.exists(main_folder_name):
        os.makedirs(main_folder_name)
    search_url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-' \
                 'bool.html&r=0&f=S&l=50&TERM1=' + search_string_1 + '&FIELD1=&co1=AND&TERM2=' + search_string_2 + '&FIELD2=&d=PTXT'
    # search_url ='http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=Ronds&FIELD1=&co1=AND&TERM2=Ronds&FIELD2=&d=PTXT'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/'
                      '1.63.6726.400 QQBrowser/10.2.2265.400',
        'Host': 'patft.uspto.gov',
        'Referer': 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html'\
                '&r=0&f=S&l=50&TERM1=Ronds&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT',
        'If-None-Match': "KQwjMJ050avfdH47mppTfvU3CBA="
    }
    # 'Referer': 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html'\
    #          '&r=0&f=S&l=50&TERM1=Ronds&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT',
    # 'X-Requested-With': 'XMLHttpRequest'
    r = s.get(search_url, headers=headers)
    text = r.text
    print('finish collecting html...')
    soup = BeautifulSoup(text, "html.parser")
    number_of_patents = int(soup.find('b').nextSibling[2:-10])
    print('The total of patents under your key words is: ' + str(number_of_patents))

    for number in range(1, number_of_patents + 1):
        print('collecting patent data' + '(' + str(number) + '/' + str(number_of_patents) + ')')
        # patent_url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2F' \
        #              'search-bool.html&r=' + str(number) + '&f=G&l=50&co1=AND&d=PTXT&s1=%22led+lamp%22&OS=%22led+' \
        #                                                    'lamp%22&RS=%22led+lamp%22'
        patent_url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r='\
                     + str(number) + '&f=G&l=50&co1=AND&d=PTXT&s1='+search_string_1+'&OS='+ search_string_1 + '&RS='+search_string_1
        get_patent_data(patent_url, headers, search_string_1)

if __name__ == '__main__':
    main()
