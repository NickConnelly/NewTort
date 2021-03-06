"""
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 43):
 * <neerajkumar@outlook.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return. 
 * If you are reading this in the second half the the 21st century, then I am at 
 * an age which won't allow me to metabolize any kind of alcohol, so please
 * treat yourself with a beer on my behalf.
 * -Neeraj Kumar
 * ----------------------------------------------------------------------------
 */
"""
from __future__ import unicode_literals

from urllib2 import Request, urlopen, URLError
from urllib import urlencode
from datetime import datetime, timedelta
import json


#from pytranslator.mstranslator.utils import Constant

#from pytranslator.mstranslator.endpoints import *
import datetime
import math
import json
import retry
import time
import urllib
import urllib2
import requests


SCOPE='http://api.microsofttranslator.com'
OAUTH_URL='https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
AZURE_TRANSLATE_API_URL='http://api.microsofttranslator.com/V2/Ajax.svc/Translate?%s'
TRANSLATE_ARRAY='http://api.microsofttranslator.com/V2/Http.svc/TranslateArray'
GRANT_CLIENT_CREDENTIALS_ONLY='client_credentials'
YOUR_APP_KEY ='263ee1af-8087-4592-bf85-5941238bdab6'
YOUR_APP_SECRET = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='



class MicrosoftTranslatorClient(object):

    def __init__(self, client_id, client_secret):
        self.client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
        self.client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
        self.last_auth_token_refresh=None
        self.auth_token = self.auth_token_please()

    def auth_token_please(self):


        data = urlencode(dict(
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = GRANT_CLIENT_CREDENTIALS_ONLY,
            scope = SCOPE
        ))

        request = Request(url=OAUTH_URL, data=data)
        response = urlopen(request)
        response = json.loads(response.read())

        self.access_key = response['access_token']
        self.expiry = int(response['expires_in'])
        print 'access token is: ' + self.access_key

        return self.access_key


    @retry.retry(Exception, tries=3, delay=5, backoff=2)
    def TranslateText(self, appId, text_array, to_lang_code):

        Access_token = self.auth_token_please["access_token"]
        self.translated_text = ""
        # Whenever there is a translate request, check if our token in still valid.
        # if valid, then its all good, continue to next step
        # if not, then get the authentication token again.
        now = datetime.datetime.now()
        if (now - self.last_auth_token_refresh).seconds > 550 :
            if not self.auth_token_please():
                return "Text could not be translated due to a recurring authentication error."
        translate_text = {
            'texts': text_array,
            'to': to_lang_code
        }
        headers = {
            'Authorization': 'Bearer ' + Access_token
        }
        translate_req = urllib2.Request(AZURE_TRANSLATE_API_URL % urllib.urlencode(translate_text),
                                    headers=headers)
        return urllib2.urlopen(translate_req).read()






"""
class MicrosoftTranslatorClient(object):
  #Handles authentication and translation for Microsoft Translator API.
  
  #Arguments:
  ## client_id: The client_id for your azure application (as a string)
  ## client_secret: The client secret for your azure application (as a string)
  
  
  def __init__(self, client_id, client_secret):
    self.client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
    self.client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
    self.last_auth_token_refresh=None
    self.auth_token = self.__GetAuthenticationToken()

  @retry.retry(Exception, tries=3, delay=5, backoff=2)
  def __GetAuthenticationToken(self):
    #Gets the authentication token for your app from azure marketplace.
    auth_args = {
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'scope': SCOPE_URL,
      'grant_type': GRANT_CLIENT_CREDENTIALS_ONLY
    }

    self.auth_token = json.loads(urllib2.urlopen(OAUTH_URL,data=urllib.urlencode(auth_args)).read())
    if self.auth_token:
      self.last_auth_token_refresh = datetime.datetime.now()
      return self.auth_token
    else:
      return None

  @retry.retry(Exception, tries=3, delay=5, backoff=2)
  def TranslateText(self, unicode_string, from_lang_code, to_lang_code):
    #Translates a given text from given language to target language.
    
    #This function tries to translate the text thrice, and if no translations could be done
    #returns an empty string.
    
    #Arguments:
      #unicode_string: The string to transalte in unicode format.
      #from_lang_code: The source language code.
      #to_lang_code: The destination language code.
    
    #Returns:
      #Translated string if succesful, ""(empty string) otherwise.
    
    
    self.translated_text = ""
    # Whenever there is a translate request, check if our token in still valid.
    # if valid, then its all good, continue to next step
    # if not, then get the authentication token again.
    now = datetime.datetime.now()
    if (now - self.last_auth_token_refresh).seconds > 550 :
      if not self.__GetAuthenticationToken():
        return "Text could not be translated due to a recurring authentication error."
    translate_text = {
      'appId': ,
      'texts': unicode_string,
      'to': to_lang_code,
    }
    headers = {
      'Authorization': 'Bearer'+ ' ' + self.auth_token['access_token']
    }
    translate_req = urllib2.Request(TRANSLATE_ARRAY % urllib.urlencode(translate_text),
                                    headers=headers)
    return urllib2.urlopen(translate_req).read()

######################################3

     def auth_token_please(self):
        token_args={
          'client_id': self.client_id,
          'client_secret': self.client_secret,
          'scope': SCOPE,
          'grant_type': GRANT_CLIENT_CREDENTIALS_ONLY
         }
        self.auth_token_please = requests.post(OAUTH_URL, params=token_args)
        r = self.auth_token_please.json()
        print r['token_type']
        self.auth_token_please = r
        if self.auth_token_please:
            self.last_auth_token_refresh = datetime.datetime.now()
            return self.auth_token_please
        else:
            return None
"""
