#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re
import time


myheader = {
    'Cookie' : 'ews_key=fea5d2421eFVD7GFbcoC9fJjhOzCkGmIAGju9-qMEW3JqTNWiJI0PYxL6FOBH7ugDtfIdKEA; ews_token=89c0fa572c6rIRGVmdobSvhS2_egY_gGaFhLAFn2K7TXmGcKpcSQuLDKC6srEWEMwl180CRmuuARYDQgFvaCnyRpjzBJk2p9vBHQkx;',
}

symbol_list = {
    "\\": "-",
    "/": "-",
    ":": "：",
    "*": "☆",
    "?": "？",
    "\"": " ",
    "<": "《",
    ">": "》",
    "|": "-",
    ".": "。",
    "\t": " ",
    "\n": " ",
}

def write_page(url, dst_file):
    r = requests.get(url, headers=myheader)
    html_element = lxml.html.document_fromstring(r.text)
    if html_element.xpath('//h2'):
        title = html_element.xpath('//h2')[0]
        author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
        content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]

        if html_element.xpath('//div[@id="oops"]') and re.search(u'送出 ', content.text_content()):
            print "送出" 
            r = requests.get(url.replace('forum','forum_report'), headers=myheader)
            html_element = lxml.html.document_fromstring(r.text)
            content = html_element.xpath('//form[@class="forum-content-report mt-3"]')[0]

        with open(dst_file, 'a') as f:
            f.write('[' + title.text_content().encode('utf-8') + '] ' + author.text_content().strip().encode('utf-8') + '\n')
            f.write(content.text_content().encode('utf-8')+'\n\n')

    
def contain(string, array):
    if isinstance(array, dict):
        return any(symbol in string for symbol in array.keys())
    elif isinstance(array, list) or isinstance(array, tuple):
        return any(symbol in string for symbol in array)
    return False


def escape_symbol(string):
    while contain(string, symbol_list):
        for char, replace_char in symbol_list.items():
            string = string.replace(char, replace_char)
    return string


if __name__ == "__main__":

    novelid_list = []
    for i in range(2,0,-1):
        r = requests.get('https://www.esjzone.cc/list-21/'+str(i)+'.html', headers=myheader)
        html_element = lxml.html.document_fromstring(r.text)
        search_result = html_element.xpath('//div[@class="col-xl-9 col-lg-8 p-r-30"]')
        if search_result:
            search_result_str = lxml.html.tostring(search_result[0])
        m = re.findall(r'detail/(\d+)\.html', search_result_str)
        novelid_list.extend(m)

    novelid_list = list(set(novelid_list))

    done_list = [line.rstrip('\n') for line in open('finished.txt')]

    for novel_id in novelid_list:

        if novel_id in done_list:
            continue 

        novel_url = 'https://www.esjzone.cc/detail/' + novel_id + '.html'
        r = requests.get(novel_url, headers=myheader)
        html_element = lxml.html.document_fromstring(r.text)

        novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
        novel_name = escape_symbol(novel_name.encode('utf-8'))
        print novel_name
        dst_filename = novel_name + '.txt'
        with open(dst_filename, 'w') as f:
            f.write(u"書名: ".encode('utf-8') + novel_name + "\n")
        with open(dst_filename, 'a') as f:
            f.write(u"URL: " + novel_url)

        novel_details_element = html_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]')[0]
        if novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div'):
            bad_divs = novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div')
            for bad_div in bad_divs:
                bad_div.getparent().remove(bad_div)
        novel_details = novel_details_element.text_content()
        with open(dst_filename, 'a') as f:
            f.write(novel_details.encode('utf-8'))
        with open(dst_filename, 'a') as f:
            f.write(u"使用的備份工具:\nhttps://github.com/ZALin/ESJ-novel-backup\n\n".encode('utf-8'))

        novel_outlink_element = html_element.xpath('//div[@class="row out-link"]')[0]
        if len(novel_outlink_element) != 0:
            outlink_list = novel_outlink_element.getchildren()
            for element in outlink_list:
                with open(dst_filename, 'a') as f:
                    f.write(element.getchildren()[0].text_content().encode('utf-8') + u":\n".encode('utf-8') + element.getchildren()[0].attrib['href'].encode('utf-8') + "\n")


        if re.search('id="details"', r.text):
            novel_description = html_element.get_element_by_id("details").text_content()
            with open(dst_filename, 'a') as f:
                f.write(novel_description.encode('utf-8'))
        else:
            with open(dst_filename, 'a') as f:
                f.write('\n\n')



        if re.search('id="chapterList"', r.text):
            chapter_list = html_element.get_element_by_id("chapterList").getchildren()
            chapter_list_without_details_tag = []
            
            for element in chapter_list:

                if element.tag == 'details':
                    for i in element.getchildren():
                        chapter_list_without_details_tag.append(i)
                else:
                    chapter_list_without_details_tag.append(element)

            for element in chapter_list_without_details_tag:
                
                with open(dst_filename, 'a') as f:
                    print element.text_content()
                    f.write(element.text_content().encode('utf-8')+'\n')
                
                if element.tag == 'a':

                    if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                        write_page(element.attrib['href'],dst_filename)
                    else:
                        with open(dst_filename, 'a') as f:
                            f.write( element.attrib['href'] + u' {非站內連結，略過}\n'.encode('utf-8'))

        done_list.append(novel_id)
        with open('finished.txt', 'a') as f:
            f.write(novel_id+'\n')
        
        



