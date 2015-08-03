import requests
from lxml import html
import time
import os


BASE_URL = 'http://anderson.kiev.ua/'
current_folder = os.getcwd()
main_local_file = 'main_local.html'
main_subfolder = 'site_pages'
index_php = '/index.php?lang=uk'
unique_local_urls = [BASE_URL]


def main():
    parse(BASE_URL)
    print '\n\n'
    for u in unique_local_urls:
        print u


def parse(url):
    print url
    page_to_parse = get_page_from_url(url)
    localazed_page, local_urls = localize_page(page_to_parse)
    print len(local_urls), ' local urls'
    save_page(localazed_page, url)

    # print '{} \t\t -- {} local urls'.format(filename, len(local_urls))

    for u in local_urls:
        if u not in unique_local_urls:
            unique_local_urls.append(u)
            if not u.endswith('.zip') and not u.endswith('.png') and not u.endswith('.jpg'):
                parse(u)


def get_page_from_url(url):
    time.sleep(0.5)
    r = requests.get(url)
    rt = r.text
    page = html.fromstring(rt)
    return page


def localize_page(page):
    local_urls = []
    a_tags = page.findall('.//a')
    a_tags_local = [url for url in a_tags if url.attrib['href'].startswith(BASE_URL)]
    for a in a_tags_local:
        url_before = a.attrib['href']
        local_urls.append(url_before)
        url_after = url_before.replace(BASE_URL, '').rstrip('/')+'.html'
        if url_after == index_php:
            url_after = url_after.replace(index_php, main_local_file)
        a.attrib['href'] = url_after
    return page, local_urls


def save_page(page, url):
    if url == BASE_URL:
        filename = main_local_file
        subfolder = main_subfolder
    else:
        # filename = url.split('/')[3].replace('/', '___') + '.html'
        filename = url.split(BASE_URL)[1].rstrip('/').replace('/', '__') + '.html'
        print 'modified filename:', filename
        subfolder = main_subfolder

    fullpath = os.path.join(current_folder, subfolder, filename)
    
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)
    with open(fullpath, 'w+') as f:
        temp = html.tostring(page)
        f.write(temp)


main()

# subfolders for main pages and child ones
# def localize()  --  anderson.kiev.ua/index.php?lang=uk
# "vystupy" links doesn't work
# dwld images
