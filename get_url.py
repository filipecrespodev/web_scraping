import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

option = Options()
driver = webdriver.Chrome(options=option)
placas = []
models = []
# option.headless = True

url = 'https://whattomine.com/gpus'
driver.get(url)

element = driver.find_elements_by_xpath("//a[@class='manufacturer--nvidia']")
for x in element:
  models.append(x.get_attribute('innerText'))

element = driver.find_elements_by_xpath("//a[@class='manufacturer--amd']")
for x in element:
  models.append(x.get_attribute('innerText'))

driver.quit()
# print(models)

url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]'
# url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia?pagina=2&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]'
# url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/nvidia?pagina=3&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]'

# url = 'https://www.kabum.com.br/hardware/placa-de-video-vga/amd-ati?pagina=1&ordem=5&limite=100&prime=false&marcas=[]&tipo_produto=[]&filtro=[]'

# time.sleep(3)

driver = webdriver.Chrome(options=option)
driver.get(url)
element = driver.find_elements_by_xpath("//*[@class='sc-fzqNqU jmuOAh']")

# for row in element:
# print(row)
row = element[0]
name = row.find_element_by_xpath("//*[@class='sc-fzoLsD gnrNhT item-nome']").get_attribute("innerHTML")
# print(element[0].get_attribute("innerText"))
# print(element[1].get_attribute("innerText"))


if name.find('NVIDIA') >= 0:
  brand = 'NVIDIA'
else:
  brand = 'AMD'

match = next((x for x in models if x in name), False)

placas.append(
  {
    'name': name,
    'link': row.find_element_by_xpath("//*[@class='sc-fzoLsD gnrNhT item-nome']").get_attribute("href"),
    'value_descout': row.find_element_by_xpath("//*[@class='sc-fznWqX qatGF']").get_attribute("innerHTML"),
    'value': row.find_element_by_xpath("//*[@class='sc-fznxsB ksiZrQ']").get_attribute("innerHTML"),
    'brand': brand,
    'model': match
  }
)

print(placas)

driver.quit()
