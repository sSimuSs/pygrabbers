import time, requests, re, shutil, os
from lxml import html
from watermark import del_watermark, add_watermark

def adding(product, parent=None, category=None):
    if 'html_url' in product:
        print(product['html_url'])
        print(product['full_name'].encode("utf-8"))
        formed_product = {}
        formed_product['name'] = product['full_name']
        formed_product['name_prefix'] = product['name_prefix']
        formed_product['description'] = product['description']
        formed_product['mini_description'] = product['micro_description']
        formed_product['category_id'] = category

        formed_product['sku'] = product['key']
        formed_product['orig_id'] = product['id']
        formed_product['color_code'] = product['color_code']
        formed_product['parent_product'] = parent

        product_page_html = html.fromstring(requests.get(product['html_url']).content)

        formed_product['brand'] = product_page_html.cssselect("ol.breadcrumbs__list li")[-1].cssselect('a')[0].cssselect('span')[0].text.strip()

        all_characs_groups = product_page_html.cssselect("table.product-specs__table tbody")
        if all_characs_groups[0].cssselect("tr.product-specs__table-spread"):
            if all_characs_groups[0].cssselect("tr.product-specs__table-spread")[0].cssselect("td")[0].cssselect(".product-specs__table-small p")[0]:
                formed_product['description'] = all_characs_groups[0].cssselect("tr.product-specs__table-spread")[0].cssselect("td")[0].cssselect(".product-specs__table-small p")[0].text.strip()
            formed_product['mini_description'] = product['description']

        if product['images']['header']:
            main_img_url = "https:" + product['images']['header']
            main_image_name = main_img_url.split('/')[-1]
            main_image_response = requests.get(main_img_url)
            if main_image_response.status_code == 200:
                os.makedirs("images/{}/".format(formed_product['orig_id']), exist_ok=True)
                path = "images/{}/{}".format(formed_product['orig_id'], main_image_name)
                formed_product['main_image'] = main_image_name
                with open(path, 'wb') as f:
                    main_image_response.raw.decode_content = True
                    shutil.copyfileobj(main_image_response.raw, f)

        formed_product['characters'] = []
        for a_characs_group in all_characs_groups:
            all_charac_trs = a_characs_group.cssselect('tr')
            for a_tr in all_charac_trs:
                if len(a_tr.cssselect('td')) == 2:
                    character_dict = {}
                    character_dict['name'] = a_tr.cssselect('td')[0].text.strip()
                    if a_tr.cssselect('td')[0].cssselect('div.product-tip-wrapper'):
                        character_dict['description'] = a_tr.cssselect('td')[0].cssselect(
                                'div.product-tip-wrapper .product-tip__content p')[1].text.strip()

                    if a_tr.cssselect('td')[1].cssselect('span.value__text'):
                        if a_tr.cssselect('td')[1].cssselect('span.value__text')[0].text:
                            character_dict['value'] = a_tr.cssselect('td')[1].cssselect('span.value__text')[
                                0].text.strip()
                    elif a_tr.cssselect('td')[1].cssselect('span.i-tip'):
                        character_dict['value'] = "yes"
                    elif a_tr.cssselect('td')[1].cssselect('span.i-x'):
                        character_dict['value'] = "no"

                    formed_product['characters'].append(character_dict)


        all_gallery = product_page_html.cssselect("div.product-gallery__shaft div.product-gallery__thumb")
        count_gallery = 1
        formed_product['gallery'] = []
        formed_product['videos'] = []
        for a_gallery in all_gallery:
            if a_gallery.xpath('@data-original') and count_gallery < 11:
                main_img_url = a_gallery.xpath('@data-original')[0]
                name = main_img_url.split('/')[-1]
                path = "images/{}/{}".format(formed_product['orig_id'], name)
                formed_product['gallery'].append(path)
                main_image_response = requests.get(main_img_url, stream=True)
                if main_image_response.status_code == 200:
                    os.makedirs("images/{}/".format(formed_product['orig_id']), exist_ok=True)
                    with open(path, 'wb') as f:
                        main_image_response.raw.decode_content = True
                        shutil.copyfileobj(main_image_response.raw, f)

                    count_gallery += 1

                    without_watermark = del_watermark(path)
                    watermarked = add_watermark(without_watermark)
                    # os.remove(image_name)
                    watermarked.convert('RGB').save(path)

            elif a_gallery.cssselect('div.video-thumb'):

                video_data = a_gallery.cssselect('div.video-thumb')[0].xpath('@data-bind')[0].strip()
                video_url = re.search(r'getThumbnail\(\'(.*?)\', \'', video_data).group(1)
                formed_product['videos'].append(video_url)

        time.sleep(1)
        return formed_product