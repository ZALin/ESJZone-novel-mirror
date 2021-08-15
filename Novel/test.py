#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re
import time


'''
r = requests.get('https://www.esjzone.cc/forum/1622140619/116313.html')
html_element = lxml.html.document_fromstring(r.text)
title = html_element.xpath('//h2')[0]
print title
author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
with open(dst_file, 'a') as f:
    f.write('[' + title.text_content().encode('utf-8') + '] ' + author.text_content().strip().encode('utf-8') + '\n')
    f.write(content.text_content().encode('utf-8')+'\n\n')

raw_input()
'''
def write_page(url, dst_file):
    r = requests.get(url)
    html_element = lxml.html.document_fromstring(r.text)
    title = html_element.xpath('//h2')[0]
    author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
    content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
    with open(dst_file, 'a') as f:
        f.write('[' + title.text_content().encode('utf-8') + '] ' + author.text_content().strip().encode('utf-8') + '\n')
        f.write(content.text_content().encode('utf-8')+'\n\n')

if __name__ == "__main__":

 
    novelid_list = []
    for i in range(35,30,-1):
        r = requests.get('https://www.esjzone.cc/list-11/'+str(i)+'.html')
        m = re.findall(r'detail/(\d+)\.html',r.text)
        novelid_list.extend(m)
    '''
    for novel_id in novelid_list:
        with open('Todo2.txt', 'a') as f:
            f.write(novel_id+'\n')
    '''
    print novelid_list
    #novelid_list = [line.rstrip('\n') for line in open('Todo2.txt')]
    #print len(novelid_list)
    done_list = [line.rstrip('\n') for line in open('finishedtest.txt')]
    print done_list

    for novel_id in novelid_list:

        if novel_id in done_list:
            continue 

    #novel_id = ''  # the novel id you want to dowload
        r = requests.get('https://www.esjzone.cc/detail/' + novel_id + '.html')
        html_element = lxml.html.document_fromstring(r.text)

        novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
        print novel_name
        #dst_filename = novel_name + ".txt"
        dst_filename = "test.txt"
        '''
        novel_details = html_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]')[0].text_content()
        with open(dst_filename, 'w') as f:
            f.write(novel_details.encode('utf-8'))


        if re.search('id="details"', r.text):
            novel_description = html_element.get_element_by_id("details").text_content()
            with open(dst_filename, 'a') as f:
                f.write(novel_description.encode('utf-8'))
        else:
            with open(dst_filename, 'a') as f:
                f.write('\n\n')



        if re.search('id="chapterList"', r.text):
            chapter_list = html_element.get_element_by_id("chapterList").getchildren()
            
            for element in chapter_list:
                
                with open(dst_filename, 'a') as f:
                    print element.text_content()
                    f.write(element.text_content().encode('utf-8')+'\n')
                
                if element.tag == 'a':

                    if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                        write_page(element.attrib['href'],dst_filename)
                    else:
                        with open(dst_filename, 'a') as f:
                            #print element.text_content()
                            f.write( element.attrib['href'] + u' {非站內連結，略過}\n'.encode('utf-8'))
        '''
        done_list.append(novel_id)
        print done_list
        with open('finishedtest.txt', 'a') as f:
           f.write(novel_id+'\n')
        





