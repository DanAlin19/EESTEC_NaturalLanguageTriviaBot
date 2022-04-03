from email import header
from urllib import response
from flask import Flask
from flask import request,jsonify
from googlesearch import search
from bs4 import BeautifulSoup,Comment
import requests
from collections import Counter
import re
import json
import urllib.request
import requests 
from num2words import num2words

app = Flask("abc")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sanity", methods=['GET'])
def init():
    return "",200

@app.route('/question', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        qname = data['question_text']
        qtype = data['question_type']
        qcat = data['question_category']
        qans = data['answer_choices']
        anstype = data['answer_type']               

        if qtype == "multiple_choice":        
            maxim = 0
            count = [0, 0, 0, 0]
            string = [0, 0, 0, 0]
            for j in search(qname,lang="en", proxy=None, advanced=False):
                url = j 
                print(url)
                html = requests.get(url, headers=headers)
                text_full = text_from_html(html)

                if anstype == "text":
                    i = 0
                    while i < 4:
                        count[i] = count[i] + text_full.count(qans[i])
                        i = i + 1
                    if( (count[0] - count[1] >= 5 and count[0] - count[2] >= 5 and count[0] - count [3] >= 5) or
                        (count[1] - count[0] >= 5 and count[1] - count[2] >= 5 and count[1] - count [3] >= 5) or
                        (count[2] - count[0] >= 5 and count[2] - count[1] >= 5 and count[2] - count [3] >= 5) or
                        (count[3] - count[0] >= 5 and count[3] - count[1] >= 5 and count[3] - count [2] >= 5) ):
                        break
                else:
                    if url.find("wiki") == -1 and url.find("pdf") == -1:
                        if qname.find("How") != -1 and int(qans[0])<100 and int(qans[1])<100 and int(qans[2])<100 and int(qans[3])<100:

                            string[0] = num2words(int(qans[0]))
                            string[1] = num2words(int(qans[1]))
                            string[2] = num2words(int(qans[2]))
                            string[3] = num2words(int(qans[3]))
                            # print(string[0], string[1], string[2], string[3])
                            text_split = re.split('. | ', text_full)
                            # print(text_split)

                            for nums in text_split:
                                i = 0
                                while i < 4:
                                    if string[i] == nums:
                                        count[i] = count[i] + 1
                                    i = i + 1
                            if( (count[0] - count[1] >= 5 and count[0] - count[2] >= 5 and count[0] - count [3] >= 5) or
                                (count[1] - count[0] >= 5 and count[1] - count[2] >= 5 and count[1] - count [3] >= 5) or
                                (count[2] - count[0] >= 5 and count[2] - count[1] >= 5 and count[2] - count [3] >= 5) or
                                (count[3] - count[0] >= 5 and count[3] - count[1] >= 5 and count[3] - count [2] >= 5) ):
                                break

                        else:
                            str = text_full
                            x = re.findall('[0-9]+', str)
                            for nums in x:
                                i = 0
                                while i < 4:
                                    if nums == qans[i]:
                                        count[i] = count[i] + 1
                                    i = i + 1
                            if( (count[0] - count[1] >= 5 and count[0] - count[2] >= 5 and count[0] - count [3] >= 5) or
                                (count[1] - count[0] >= 5 and count[1] - count[2] >= 5 and count[1] - count [3] >= 5) or
                                (count[2] - count[0] >= 5 and count[2] - count[1] >= 5 and count[2] - count [3] >= 5) or
                                (count[3] - count[0] >= 5 and count[3] - count[1] >= 5 and count[3] - count [2] >= 5) ):
                                break    
                            print(x)
            i = 0
            while i < 4:
                if count[i] > maxim:
                    maxim = count[i]
                    poz = i
                i = i + 1
            print(qans[poz])
            i = 0
            while i < 4:
                print(count[i])
                i = i + 1
        
            return jsonify({'answer' : qans[poz]})


        else:
            for j in search(qname,lang="en", proxy=None, advanced=False):
                url = j
                html = requests.get(url, headers=headers)
                text_full = text_from_html(html)
                siruri = [0, 0, 0, 0]
                if qname.find("When") != -1:
                    cate = -1
                    x = re.findall('[0-9]+', text_full)
                    for key in x:
                        if int(key) >= 100 and int(key) <= 3000:
                            ok = 1
                            j = 0
                            while j <= cate:
                                if siruri[j] == key:
                                    ok = 0
                                    break
                                j = j + 1
                            if ok == 1:
                                cate = cate + 1 
                                siruri[cate] = key
                        if cate == 3:
                            break
                # else if qname.find("Who") != -1

                break
            count = [0, 0, 0, 0]
            print(siruri[0], siruri[1], siruri[2], siruri[3])
            for j in search(qname,lang="en", proxy=None, advanced=False):
                url = j 
                print(url)
                html = requests.get(url, headers=headers)
                text_full = text_from_html(html)
                str = text_full
                x = re.findall('[0-9]+', str)
                for nums in x:
                    i = 0
                    while i < 4:
                        if nums == siruri[i]:
                            count[i] = count[i] + 1
                        i = i + 1
                if( (count[0] - count[1] >= 5 and count[0] - count[2] >= 5 and count[0] - count [3] >= 5) or
                    (count[1] - count[0] >= 5 and count[1] - count[2] >= 5 and count[1] - count [3] >= 5) or
                    (count[2] - count[0] >= 5 and count[2] - count[1] >= 5 and count[2] - count [3] >= 5) or
                    (count[3] - count[0] >= 5 and count[3] - count[1] >= 5 and count[3] - count [2] >= 5) ):
                    break    
                print(x)
            i = 0
            maxim = 0
            while i < 4:
                if count[i] > maxim:
                    maxim = count[i]
                    poz = i
                i = i + 1 
            i = 0
            while i < 4:
                print(count[i])
                i = i + 1   
            return jsonify({'answer' : siruri[poz]})
            
    else:
        return 'Content-Type not supported!'

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body.text, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)