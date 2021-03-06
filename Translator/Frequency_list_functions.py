#-*- coding: utf-8 -*-

#import re
#import codecs
#from django.utils.encoding import smart_str
import collections
import os
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import urllib2
import urllib
import nltk.data
from Translator.mstranslator.client import MSTranslator
from Translator.mstranslator.client import MSTranslatorAccessKey
import requests
from lxml import etree
from django.shortcuts import render_to_response
from urllib import urlencode
from urllib2 import Request, urlopen, URLError
#import json
import os
#import xml.etree.ElementTree as ET
from urllib2 import Request, urlopen, URLError
from httplib import HTTPResponse
import sys
from io import StringIO
from datetime import datetime, timedelta
from operator import itemgetter



def Create_xml(Array, from_language, to_language):
    # Creates an XML tree containing all of the information that Microsoft API needs to translate the Array
    root = etree.Element('TranslateArrayRequest')
    AppId = etree.SubElement(root, 'AppId')
    From = etree.SubElement(root, 'From')
    From.text = str(from_language)
    Options = etree.SubElement(root, 'Options')
    Category = etree.SubElement(Options, 'Category', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    ContentType = etree.SubElement(Options, 'ContentType', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    ContentType.text = 'text/plain'
    ReservedFlags = etree.SubElement(Options, 'ReservedFlags', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    State = etree.SubElement(Options, 'State', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    Uri = etree.SubElement(Options, 'Uri', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    User = etree.SubElement(Options,'User', xmlns="http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2")
    Texts = etree.SubElement(root, 'Texts')
    #string = etree.SubElement(Texts, 'string', xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays")
    stringlist = []
    stringlist.append(Array)
    for i in stringlist:
        string = etree.SubElement(Texts, 'string', xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays")
        i = i.encode('UTF-8')
        i = unicode(i, 'UTF-8', errors='replace')
        string.text = i
      # Changed the above from str(i) to i
    To = etree.SubElement(root, 'To')
    To.text = str(to_language)
    s = etree.tostring(root, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    return s

def maketranslate(msarray):
    msarraylist = []
    msarraylist.append(msarray)
    client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
    client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
    #Client secret and ID are linked to my Microsoft account, and never change.
    MS_TRANSLATOR_KEY = MSTranslatorAccessKey(client_id, client_secret)
    key = MS_TRANSLATOR_KEY
    translator = MSTranslator(key)
    headers = {'Authorization': translator.get_authorization_string(), 'content-type': 'application/xml'}
    XML_Doc = Create_xml(Array=msarray, from_language = 'en', to_language = 'de')
    data = XML_Doc
    W = requests.post(url='http://api.microsofttranslator.com/V2/Http.svc/TranslateArray2', data=data, headers=headers)
    W = etree.parse(StringIO(W.text))
    root = W.getroot()
    TranslationandAlignmentlist = []
    TranslationArray = []
    AlignmentArray = []
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}TranslatedText':
            translations = element.text
            translations = translations.encode('UTF-8')
            TranslationArray.append(translations)
            print TranslationArray
    for element in root.iter():
        if element.tag == '{http://schemas.datacontract.org/2004/07/Microsoft.MT.Web.Service.V2}Alignment':
            if element.text == None:
                AlignmentArray.append('No Alignment Data')
            else:
                translations = element.text
                AlignmentArray.append(translations)
    #[x for x in AlignmentArray if x is not None]
    TranslationandAlignmentlist.append(TranslationArray)
    TranslationandAlignmentlist.append(AlignmentArray)
    TranslationandAlignmentlist.append(msarraylist)
    #print etree.tostring(W, xml_declaration=True, pretty_print=True, encoding='UTF-8')
    Translation = TranslationandAlignmentlist
    return Translation

def mash_em(Source_text, Translated_text, Alignment):
    #Creates a list of every word in the Translated_text, thus maintaining it's index
    IndexList1 = []
    Translated_text = Translated_text.strip("[]'")
    print Alignment
    a = Alignment.strip("[]'")
    print a
    a = a.split(' ')
    print a
    for listy in a:
        a = listy.split('-')
        IndexList1.append(a)
    print IndexList1
    # Separate the Source Text indexes and the Translation indexes and saves them together as a list within IndexList1
    # IndexList1 is a list of lists. Each nested list contains the source text indexes in i[0] and the corresponding translation text alignment in i[1]
    Source_list = []
    Translated_list = []
   # print IndexList1
    for boom in IndexList1:
        if len(boom)>1 and boom != 'No Alignment Data':
            Source_list.append(boom[0])
            Translated_list.append(boom[1])
        else:
            Source_list.append('No Source Alignment')
            Translated_list.append('No Translation Alignment')
       # This takes the Source Text indexes from IndexList1 and appends them the recently created Source_list, and the Translated Text indexes from IndexList1 and appends them the recently created Translated_list
    Source_list_new = []
    Translated_list_new = []
    for i in Source_list:
        if len(i)>1 and i != 'No Source Alignment':
            i = i.split(':')
            SourceString = Source_text[int(i[0]):(int(i[1]) + 1)]
            Source_list_new.append(SourceString.capitalize())
	    #First line of the for loop splits the start and end indices of Source text, because the alignment information cannot be interpreted as a string
	    #Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Source_list_new
        else:
            Source_list_new.append(Source_list[0:])
    for i in Translated_list:
        if len(i)>1 and i != 'No Translation Alignment':
            i = i.split(':')
            TranslatedString = Translated_text[int(i[0]):(int(i[1]) + 1)]
            Translated_list_new.append(TranslatedString.capitalize())
	    #First line of the for loop splits the start and end indices of Translated text, because the alignment information cannot be interpreted as a string
	    #Second line joins all of the words for the given alignment index, and appends the newly formed string to the recently created Translated_list_new
        else:
            Translated_list_new.append(Translated_text_list[0:])
    Zipped_lists = []
    Zipped_lists = zip(Source_list_new, Translated_list_new)
    #Zip works because the index of the source text in Source_list_new is always going to match the index of the translation text it corresponds to in Translated_list_new
    return Zipped_lists


def frequency_counter(Zipped_lists):
    counter=collections.Counter(Zipped_lists)
    #collections.Counter counts occurrences of an instance in a list
    OrganizedTranslations = []
    for k,v in sorted(counter.items()):
	TemporaryList = []
        #The Dictionary that resulted from counting 'NewJ' is sorted, and iterated through
        #k = k.encode('UTF-8')
        TemporaryList.append(k[0])
        TemporaryList.append(k[1])
        TemporaryList.append(v)
	OrganizedTranslations.append(TemporaryList)
    FinalOrganizedTranslations = sorted(OrganizedTranslations, key=itemgetter(2), reverse=True)
    print FinalOrganizedTranslations
    return FinalOrganizedTranslations

def words_from_line(line):
    line = line.decode('UTF-8')
    line = (line.rstrip('\n'))
    #return re.split('(?:\s|[*\r,.:#@()+=<>$;"?!|\[\]^%&~{}«»–])+', line)
    #return re.split('[^a-zA-ZäöëüßÄËÖÜß]+', line)
    return re.compile("(?!['_])(?:\W)+", flags=re.UNICODE).split(line)


def _demo_show_text( text ):
    lines = text.splitlines()
    blocks = []
    this_lines = []
    for line in lines:
        if line == '':
            if this_lines != []:
                blocks.append( '\n'.join( this_lines ) )
                this_lines = []
        else:
            this_lines.append( line )
    if this_lines != []:
        blocks.append( ''.join( this_lines ) )
    normalizer = Normalizer('en')
    res = []
    for b in blocks:
        pattern = re.compile(r'\b([a-zA-Z]+)\b')
        res.append( re.sub(pattern, lambda x: _demo_show_normalized( normalizer, x.group(1) ), b) )
    Final = "\n".join( x+"\n" for x in res )
    return render_to_response('Demo_text.html', {'Final': Final})

def converted(request, doc_id):
#    filename = os.path.join(settings.PATH_TO_CONVERTED, doc_id, 'text')
#    if '/' in doc_id or not os.path.exists(filename):
#        filename = '/dev/null'
#    f = filename
     return f

def sentences_in_f(textfile):
    lines = [line.strip() for line in open('textfile')]
    Text_list = start.splitlines(True)
    return Text_list

#def docsplitter(Document):
#    SourceTextArray = []
#    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#    fp = open(Document)
#    data = fp.read()
#    data = data.decode('utf-8')
#    SourceTextArray.append(tokenizer.tokenize(data))
#    SourceTextArray = SourceTextArray[0]
#    return SourceTextArray
