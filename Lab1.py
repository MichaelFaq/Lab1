from PIL import Image, ImageStat
import cStringIO
import urllib
import lxml.html as html
from lxml.html import parse, fromstring, etree
from math import trunc
import gevent.monkey
import time
import coverage
gevent.monkey.patch_socket()

f = open('base.xml', 'w')
f.write('<root>')
f.write('<url>')
f.write('http://prikol.bigmir.net/all/pictures/')
f.write('</url>')
f.write('<url>')
f.write('http://pobedakino.com.ua/')
f.write('</url>')
f.write('<url>')
f.write('http://prikol.bigmir.net/all/pictures/')
f.write('</url>')
f.write('<url>')
f.write('http://pobedakino.com.ua/')
f.write('</url>')
f.write('</root>')
f.close()


def take_url(url_html):
    see_html = urllib.urlopen(url_html.text_content()).read()

    tree = html.parse(cStringIO.StringIO(see_html), etree.HTMLParser())
    s = etree.tostring(tree.getroot())

    i = 0
    mas_brightness = []
    for imgl in fromstring(s).cssselect('img'):
        if imgl.get('src') is not None:
            if imgl.get('src').find('.jpg') != -1 \
                or imgl.get('src').find('.jpeg') != -1 \
                    or imgl.get('src').find('.png') != -1\
                    or imgl.get('src').find('.bmp') != -1:
                if imgl.get('src').find('http://') != -1:
                    url = imgl.get('src')
                else:
                    url = 'http:'+imgl.get('src')

                # print '%s' % (URL)
                try:
                    file = cStringIO.StringIO(urllib.urlopen(url).read())
                    img = Image.open(file)
                    # img.save("pil-basic"+str(i)+".png")
                    i = i + 1
                    r, g, b = ImageStat.Stat(img).mean[0], \
                        ImageStat.Stat(img).mean[1], \
                        ImageStat.Stat(img).mean[2]
                    GetBrigtness = 0.3*r + 0.59*g + 0.11*b
                    mas_brightness.append(GetBrigtness)
                except IOError:
                    pass

    if (len(mas_brightness) != 0):
        min = mas_brightness[0]
        max = min
        for z in mas_brightness:
            if (z > max):
                max = z
            if (z < min):
                min = z

        mas_k = [0, 0, 0]
        # mas_el = [[],[],[]]
        delit = trunc((max - min) // 3) + 1
        for z in mas_brightness:
            ind = trunc((z - min) // delit)
            mas_k[ind] = mas_k[ind] + 1
        return mas_k


def to_xml_file(res):
    f = open('result.xml', 'a')
    for el in res:
        if el is not None:
            for j in range(len(el)):
                f.write(' <brightnees'+str(j+1)+'> ')
                f.write(el[j].__str__())
                f.write(' </brightnees'+str(j+1)+'> ')
    f.close()


def async_main_function(name_xml):
    start_async = time.time()
    threads = []
    result = []
    f = open('result.xml', 'w')
    f.write('<root>')
    f.close()

    xml_tree = etree.parse(name_xml)
    xml_s = etree.tostring(xml_tree.getroot())
    for p in fromstring(xml_s).cssselect('url'):
        threads.append(gevent.spawn(take_url, p))
    gevent.joinall(threads)
    for result_parsing in threads:
        result.append(result_parsing.value)
    to_xml_file(result)
    f = open('result.xml', 'a')
    f.write('</root>')
    f.close()
    return time.time() - start_async


def sync_main_function(name_xml):
    start_sync = time.time()
    f = open('result.xml', 'w')
    f.write('<root>')
    f.close()
    result = []

    xml_tree = etree.parse(name_xml)
    xml_s = etree.tostring(xml_tree.getroot())
    for p in fromstring(xml_s).cssselect('url'):
        result.append(take_url(p))
    to_xml_file(result)
    f = open('result.xml', 'a')
    f.write('</root>')
    f.close()
    return time.time() - start_sync


print async_main_function('base.xml')
print sync_main_function('base.xml')


#print coverage.report()