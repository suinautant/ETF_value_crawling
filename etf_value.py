import urllib.request
import bs4
import time

url_values = [
    ['EWY', '239681/'],
    ['IDEV', '286762/'],
    ['IEMG', '244050/'],
    ['IEUR', '264617/'],
    ['IPAC', '264619/'],
    ['AAXJ', '239601/'],
    ['IVV', '239726/'],
    ['MCHI', '239619/'],
    ['INDA', '239659/'],
    ['EWT', '239686/'],
    ['EWS', '239678/'],
    ['EWM', '239669/'],
    ['EIDO', '239661/'],
    ['EPHE', '239675/'],
    ['TUR', '239689/'],
    ['EIS', '239663/'],
    ['KSA', '271542/'],
    ['QAT', '264273/'],
    ['UAE', '264275/'],
    ['ERUS', '239677/'],
    ['EWZ', '239612/'],
    ['THD', '239688/']
]

etf_db_list = ['VNM', 'AOR']

def get_bs_obj(etf_code):
    url = "https://www.ishares.com/us/products/" + etf_code
    html = urllib.request.urlopen(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser")
    return bs_obj

def get_bs_obj_etfdb(etf_code):
    # url = "https://etfdb.com/etf/" + etf_code + "/"
    url = "https://etfdb.com/etf/" + etf_code + "/#etf-ticker-valuation-dividend"
    html = urllib.request.urlopen(url)
    bs_obj = bs4.BeautifulSoup(html, "html.parser")
    return bs_obj

# PE, PBR 추출
def get_value(etf_name, etf_code):
    bs_obj = get_bs_obj(etf_code)

    # comment 20201016
    # div_pe = bs_obj.find("div", {"class":"float-left in-left col-priceEarnings"})
    # div_pb = bs_obj.find("div", {"class":"float-left in-right col-priceBook"})
    div_pe = bs_obj.find("div", {"class":"col-priceEarnings"})
    div_pb = bs_obj.find("div", {"class":"col-priceBook"})

    date = div_pe("span", {"class":"as-of-date"})
    span_pe_data = div_pe("span", {"class":"data"})
    span_pb_data = div_pb("span", {"class":"data"})
    return etf_name, date[0].text, span_pe_data[0].text, span_pb_data[0].text

def get_value_etfdb(etf_code):
    bs_obj = get_bs_obj_etfdb(etf_code)

    # 20200128 이전 크롤링
    # result = bs_obj.find("div", {"class":"panel-collapse collapse", "id":"valuation-collapse"})
    # result = result.find("span", {"class":"relative-metric-bubble-data"})

    # 20200128 이후 크롤링
    result = bs_obj.find("div", {"class": "valuation-row"})
    result = result.find("span", {"class": "relative-metric-bubble-data"})

    return etf_code, result.text

# 파일명을 년도월일_시간분초 형식으로 생성
def get_file_name_as_date():
    t = time.localtime()
    file_name = "%04d%02d%02d_%02d%02d%02d.txt" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return file_name

##########################
# MAIN
##########################
file_name = get_file_name_as_date()

tmp = file_name.partition('.txt')
file_name2 = "%s_input.txt" % (tmp[0])
f_input = open(file_name2,"a")

etf_name, date, pe, pb = get_value(url_values[0][0], url_values[0][1])
data_input = "%s\n\n" % (date.strip())
f_input.write(data_input)

# iShares Homepage crawling
for url_value in url_values:
    etf_name, date, pe, pb = get_value(url_value[0], url_value[1])

    data_input = "%s\t%s\t" % (pe.strip(), pb.strip())

    # for debug
    # print(data_input)
    f_input.write(data_input)

# etfDB Homepage crawling
for i in etf_db_list:
    result_name, result_data = get_value_etfdb(i)
    result = "%s\t\t" % (result_data.strip())

    # for debug
    # print(result)
    f_input.write(result)

f_input.close()

