# -*- coding: utf-8 -*-
try:
    # python 2
    from urllib2 import Request, urlopen, quote
except ImportError:
    # python 3
    from urllib.request import Request, urlopen, quote

try:
    # python 2
    from htmlentitydefs import name2codepoint
except ImportError:
    # python 3
    from html.entities import name2codepoint

import re
import os
import subprocess
import logging


GOOGLE_SCHOLAR_URL = "https://scholar.google.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

FORMAT_BIBTEX = 4
FORMAT_ENDNOTE = 3
FORMAT_REFMAN = 2
FORMAT_WENXIANWANG = 5


logger = logging.getLogger(__name__)


def query(searchstr, outformat=FORMAT_BIBTEX, allresults=False):
    """Query google scholar.
    This method queries google scholar and returns a list of citations.
    Parameters
    ----------
    searchstr : str
        the query
    outformat : int, optional
        the output format of the citations. Default is bibtex.
    allresults : bool, optional
        return all results or only the first (i.e. best one)
    Returns
    -------
    result : list of strings
        the list with citations
    """
    logger.debug("Query: {sstring}".format(sstring=searchstr))
    searchstr = '/scholar?q='+quote(searchstr)
    url = GOOGLE_SCHOLAR_URL + searchstr
    cookies = get_cookie(outformat)
    header = HEADERS
    #header['Cookie'] = "GSP=CF=%d" % outformat
    # header['Cookie'] = cookies
    header['Cookie'] = cookies
    request = Request(url, headers=header)
    response = urlopen(request)
    html = response.read()
    html = html.decode('utf8')
    # print html
    # grab the links
    tmp = get_links(html, outformat)
    # print tmp

    # follow the bibtex links to get the bibtex entries
    result = list()
    if not allresults:
        tmp = tmp[:1]
    for link in tmp:
        url = GOOGLE_SCHOLAR_URL+link
        request = Request(url, headers=header)
        response = urlopen(request)
        bib = response.read()
        bib = bib.decode('utf8')
        result.append(bib)
    return result

def get_links(html, outformat):
    """Return a list of reference links from the html.
    Parameters
    ----------
    html : str
    outformat : int
        the output format of the citations
    Returns
    -------
    List[str]
        the links to the references
    """
    if outformat == FORMAT_BIBTEX:
        refre = re.compile(r'<a href="https://scholar.googleusercontent.com(/scholar\.bib\?[^"]*)')
    elif outformat == FORMAT_ENDNOTE:
        refre = re.compile(r'<a href="https://scholar.googleusercontent.com(/scholar\.enw\?[^"]*)"')
    elif outformat == FORMAT_REFMAN:
        refre = re.compile(r'<a href="https://scholar.googleusercontent.com(/scholar\.ris\?[^"]*)"')
    elif outformat == FORMAT_WENXIANWANG:
        refre = re.compile(r'<a href="https://scholar.googleusercontent.com(/scholar\.ral\?[^"]*)"')
    reflist = refre.findall(html)
    # escape html entities
    reflist = [re.sub('&(%s);' % '|'.join(name2codepoint), lambda m:
                      chr(name2codepoint[m.group(1)]), s) for s in reflist]
    return reflist

def get_cookie(format_bib):
    f=open(r'cookie.txt','r')#
    # cookies={}#
    cookies = f.read().strip('\n').split("GSP")
    GSP = cookies[1].split(":")

    # print len(GSP)

    GSP[0] = "GSP=CF=%d:" % format_bib

    result = cookies[0] + GSP[0] #change GSP value to CF=FORMAT_BIBTEX to get links
    for i in range(1, len(GSP)):
        result += GSP[i]+':'

    # print result
    # for line in f.read().split(';'):   #
    #     #
    #     name,value=line.strip().split('=',1)
    #     cookies[name]=value  #

    return result

if __name__ == "__main__":
    import textract
    import sys
    import time
    import random

    # print get_cookie(FORMAT_BIBTEX)

    if len(sys.argv)<3:
        print 'Syntax error'
        print '$ python ref_parser.py sourcefile outputfile'
        sys.exit(0)
    text = textract.process(sys.argv[1])
    text = text.strip()
    text = text.split('[')

    bibs = []
    for tex in reversed(text): # loop backward to get all references
        tex_split = tex.split(']')
        if len(tex_split)<2:
            continue
        index = tex_split[0]
        ref = tex_split[1]
        if not index.isdigit():
            continue
        # print index
        # print ref
        print '[%s]'%index + ' in process'
        try:
            bibtex = query(ref, FORMAT_BIBTEX) # 4 stands for FORMAT_BIBTEX
            bibs.append(bibtex[0])
        except:
            print 'HTTP error happened in ' + '[%s]'%index
            continue
        # print bibtex[0]

        if index=='1': # stop until we finish reference [1]
            break

        time.sleep(random.randint(15,21))

    out = open(sys.argv[2],'w')
    for bib in reversed(bibs): # print results from head to tail
        # print bib
        out.write(bib.encode('ascii','ignore').encode('utf-8'))
    # print get_cookie(FORMAT_BIBTEX)
    # text = 'J. Li, X. Chen, M. Li, P. P. C. Lee, and W. Lou. Secure dedupli-cation with efficient and reliable convergent key management. TPDS,25(6):1615–1625, 2014.'
    # print query(text)[0]
