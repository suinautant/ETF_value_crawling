# ETF_value_crawling
ETF PE/PBR crawling

# Error
20201016 실행시 오류
Traceback (most recent call last):
  File "etf_value.py", line 85, in <module>
    etf_name, date, pe, pb = get_value(url_values[0][0], url_values[0][1])
  File "etf_value.py", line 52, in get_value
    date = div_pe("span", {"class":"as-of-date"})
TypeError: 'NoneType' object is not callable

