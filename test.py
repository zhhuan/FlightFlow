from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://flight.qunar.com/schedule/fsearch_list.jsp?departure=%E5%8C%97%E4%BA%AC&arrival=%E4%B8%8A%E6%B5%B7")
soup = BeautifulSoup(html)
print(soup.body)
# results = soup.find('div',{'class':'result_content'}).findAll('li')
# for result in results:
#     print(result.get_text())
# # details = soup.find('dl',{'class':'state_detail'}).findAll('span')
# # print(details[1].get_text())
# # print(details[5].get_text().strip()[5:])
# # print(details[2].get_text().strip()[5:])
# # print(details[4].get_text().strip()[3:])
# # print(details[6].get_text().strip()[5:16])
# # print(details[6].get_text().strip()[16:])
# for detail in details:
#     print(detail.get_text())


