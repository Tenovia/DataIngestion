from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost
#from facebook_business.adobjects.campaign import Page

import json
import boto3
import datetime
import csv
import importtos3check
app_id = '<app_id>'
app_secret = '<app_secret>'
access_token ='<access_token>'
FacebookAdsApi.init(app_id, app_secret, access_token)
fields = {
    "data": [],
    "paging": {}
}
params = {
   'period':'days_28',
   'date_preset':'last_7d',
   'metric':['page_content_activity_by_action_type_unique','page_impressions','page_impressions_unique','page_impressions_organic_unique','page_impressions_viral_unique','page_impressions_nonviral','page_engaged_users']
  }
metric=['page_content_activity_by_action_type_unique']

def page_insights():
    
    
    id='553748511770269'
    
    post=Page(id).get_insights(params=params)
    #for i in range(len(postid)):
    print(post)
    #dic_post=dict(post).json.dumps()
    '''for keys,item in post[1].items():     #converting to dictionary           
      #print(item)
      dic_post[keys]=item'''
    #print(dic_post)
page_insights()
