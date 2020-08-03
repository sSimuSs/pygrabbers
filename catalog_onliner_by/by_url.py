import requests
from parser import adding

url = input("Enter URL:")
'''
Examples:
* https://catalog.onliner.by/mobile - url for parsing category (mobile in this case);
* https://catalog.onliner.by/mobile?mfr%5B0%5D=apple - url for parsing category with filters (Apple mobiles in this case);
    ** https://catalog.onliner.by/mobile?mfr%5B0%5D=apple&m_mem_flash%5Bfrom%5D=128gb&m_mem_flash%5Bto%5D=128gb - Apple 
    mobiles with 128GB flash memory
'''

path = url.replace("https://catalog.onliner.by/", "")
if not "?" in str(path):
    get_max_page = requests.get('https://catalog.api.onliner.by/search/' + str(path) + '?group=1').json()
else:
    get_max_page = requests.get('https://catalog.api.onliner.by/search/' + str(path) + '&group=1').json()
if get_max_page and 'total' in get_max_page:
    print("Found product(s): {}".format(get_max_page['total'] + 1))
    for page in range(get_max_page['page']['last']):
        print("--------- PAGE " + str(page + 1) + " -----------")
        if not "?" in str(path):
            all_data = requests.get(
                'https://catalog.api.onliner.by/search/' + str(path) + '?group=1&page=' + str(page + 1)).json()
        else:
            all_data = requests.get(
                'https://catalog.api.onliner.by/search/' + str(path) + '&group=1&page=' + str(page + 1)).json()
        for product in all_data['products']:
            parent_product = adding(product, category=None)
            for child_product in product['children']:
                adding(child_product, parent=parent_product, category=None)
else:
    print("Incorrect url. (see examples)")
