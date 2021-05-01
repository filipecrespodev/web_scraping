import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

p = {}
list_url = {
  'kabum': {
    'asus': {
      '3060': {'url': 'https://www.kabum.com.br/produto/147801/placa-de-v-deo-asus-tuf-rtx3060-o12g-gaming-90yv0gc0-m0na00'},
      '3070': {'url': 'https://www.kabum.com.br/produto/128634/placa-de-video-asus-nvidia-geforce-rtx-3070-8gb-'},
      '3080': {'url': 'https://www.kabum.com.br/produto/121chipart138/placa-de-v-deo-asus-nvidia-geforce-rtx3080-10gb-gddr6-tuf-rtx3080-10g-gaming'},
      '3090': {'url': 'https://www.kabum.com.br/produto/128026/placa-de-v-deo-asus-nvidia-geforce-rtx-3090-24gb-gddr6x-rog-strix-rtx3090-o24g-gaming-'}
    },
    'Gigabyte': {
      '3060Ti': {'url': 'https://www.kabum.com.br/produto/131949/placa-de-v-deo-gigabyte-nvidia-geforce-rtx-3060-ti-8gb-gaming-oc-pro-gv-n306tgamingoc-pro-8gd'}, 
      '3070': {'url': 'https://www.kabum.com.br/produto/130912/placa-de-v-deo-gigabyte-nvidia-aorus-geforce-rtx-3070-master-8g-gddr6-gv-n3070aorus-m-8gd'},
    },
    'Msi': {
      '3070': {'url': 'https://www.kabum.com.br/produto/130381/placa-de-v-deo-msi-geforce-rtx-3070-ventus-2x-oc'},
    },
    'Zotac': {
      '3060Ti': {'url': 'https://www.kabum.com.br/produto/131574/placa-de-v-deo-zotac-nvidia-geforce-rtx-3060ti-twin-edge-oc-8gb-gddr6-zt-a30610h-10m'}
    }
  },
  'pichau': {
    'Galax': {
      '2060': {'url': 'https://www.pichau.com.br/hardware/placa-de-video/placa-de-video-galax-geforce-rtx-2060-6gb-gddr6-1-click-oc-192-bit-26nrl7hpx7oc'},
      '3060': {'url': 'https://www.pichau.com.br/hardware/placa-de-video/placa-de-video-galax-geforce-rtx-3060-12gb-gddr6-1-click-oc-192-bit-36nol7md1voc'},
    },
    'Zotac': {
      '3060': {'url': 'https://www.pichau.com.br/hardware/placa-de-video/placa-de-video-zotac-geforce-rtx-3060-ti-twin-edge-8gb-gddr6-256-bit-zt-a30610e-10m'},
    },
  },
  'terabyteshop':{
    'Galax': {
      '2060': {'url': 'https://www.terabyteshop.com.br/produto/10304/placa-de-video-galax-geforce-rtx-2060-1-click-oc-6gb-26nrl7hpx7oc-gddr6-pci-exp'},
    },
    'Asus': {
      '3060': {'url': 'https://www.terabyteshop.com.br/produto/17268/placa-de-video-asus-geforce-rtx-3060-12gb-gddr6-192bit-90yv0gb2-m0na00'},
    },
  },
  'amazon': {
    'Asus': {
      '3060Ti': {'url': 'https://www.amazon.com.br/Placa-video-geforce-3060ti-rog-strix-rtx3060ti-o8g-gaming/dp/B08NW3TVRT/ref=pd_sbs_5?pd_rd_w=FEbyk&pf_rd_p=77d06585-886e-40b6-9b89-9436576cc5c0&pf_rd_r=SJC53M5NJPRECNYJC1W0&pd_rd_r=94ee1d12-1d2f-41dc-8a4e-83b0c3b55acd&pd_rd_wg=CwKfX&pd_rd_i=B08NW3TVRT&psc=1'}
    },
    'Zotac': {
      '3060': {'url': 'https://www.amazon.com.br/refrigera%C3%A7%C3%A3o-IceStorm-ventilador-congelamento-ZT-A30600H-10M/dp/B08W8DGK3X/ref=pd_sbs_12?pd_rd_w=oWzpD&pf_rd_p=77d06585-886e-40b6-9b89-9436576cc5c0&pf_rd_r=5AQBD36DW1GK2QE6GF5C&pd_rd_r=91c742f6-eeb6-4408-913d-2f0c280ae8e0&pd_rd_wg=ENgtQ&pd_rd_i=B08W8DGK3X&psc=1'},
    },
    'Gainward': {
      '3060': {'url': 'https://www.amazon.com.br/RTX3060-256BITS-GAINWARD-PALIT-NE63060019K9-190AU/dp/B08X4Y9FQN/ref=pd_vtp_3?pd_rd_w=xqyK8&pf_rd_p=460b1bd2-2dd3-4463-8569-0282c9641107&pf_rd_r=5AQBD36DW1GK2QE6GF5C&pd_rd_r=91c742f6-eeb6-4408-913d-2f0c280ae8e0&pd_rd_wg=ENgtQ&pd_rd_i=B08X4Y9FQN&psc=1'},
    }
  },
  'ibyte': {
    'Asus': {
      '1650': {'url': 'https://www.ibyte.com.br/placa-de-video-asus-tuf-gaming-gtx-1650-4gb-gddr6-128-bit-tuf-gtx1650-4gd6-gaming/p'}
    },
  },
  'chipart': {
    'Asus': {
      '3070': {'url': 'https://www.chipart.com.br/placa-de-video-pci-e-8gb-gddr6-asus-rtx-3070-dual-rtx3070-8g'}
    },
  },
}

option = Options()
# option.headless = True

def source(shop, brand, type):
  url = list_url[shop][brand][type]['url']
  driver = webdriver.Chrome(options=option)
  driver.get(url)

  try:
    if shop == 'kabum':
      element = driver.find_element_by_xpath("//span[@class='preco_desconto']//span//span//strong")
      value_with_descout = element.get_attribute('innerHTML')

    elif shop == 'pichau':
      element = driver.find_element_by_xpath("//div[@class='stock available']//span")
      element = driver.find_element_by_xpath("//span[@class='price-boleto']//span")
      value_with_descout = element.get_attribute('innerHTML')
      value_with_descout = value_with_descout.replace("à vista ","")

    elif shop == 'terabyteshop':
      element = driver.find_element_by_xpath("//p[@id='valVista']")
      value_with_descout = element.get_attribute('innerHTML')

    elif shop == 'amazon':
      element = driver.find_element_by_xpath("//span[@id='priceblock_ourprice']")
      value_with_descout = element.get_attribute('innerHTML')

    elif shop == 'ibyte':
      element = driver.find_element_by_xpath("//strong[@class='skuPrice']")
      value_with_descout = element.get_attribute('innerHTML')

    elif shop == 'chipart':
      element = driver.find_element_by_xpath("//span[@class='total']")
      value_with_descout = element.get_attribute('innerHTML')

  except NoSuchElementException:
    value_with_descout = 0
  driver.quit()
  return value_with_descout

for j in list_url:
  p[j] = {}
  for i in list_url[j]:
    p[j][i] = {}
    for k in list_url[j][i]:
      p[j][i][k] = source(j, i, k)

js = json.dumps(p)
fp = open('placas_out.json', 'w')
fp.write(js)
fp.close()
