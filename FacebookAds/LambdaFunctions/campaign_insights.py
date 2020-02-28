from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
import json
import boto3
import datetime
import csv

import importtos3
app_id = '417313085526905'
app_secret = 'cac5607ffca31ffadb3633063121b2d1'
access_token = 'EAAF7i0Y5E3kBADG71vJ0N6FQPOyC947lGLfQoKZCMkXkE18ZAEjPRfbJRGfWxaCgt9F93uvS3sDrPFR59LO0gtIdiCzsXLUvxeBm6f0XXdiESakgZBBRWWaWpltTHIDmXG4dxyv7lvZBfj2rXlSdr9RYcplmFwVz1WwVQZCLnqjTFGnZCMTd6MVZBTl7ZAynljIZD'
FacebookAdsApi.init(app_id, app_secret, access_token)
def campaign_insights():
    today=datetime.date.today()
    fields1=['account_name','campaign_name', 'campaign_id', 'reach','unique_outbound_clicks_ctr:outbound_click', 'cost_per_action_type:offsite_conversion.custom.118660332158323', 'unique_actions:offsite_conversion', 'date_start', 'unique_actions:post_engagement', 'cost_per_action_type:post_reaction', 'cost_per_outbound_click:outbound_click', 'action:post_engagement', 'inline_link_clicks', 'cost_per_unique_action_type:page_engagement', 'unique_actions:landing_page_view', 'action:post', 'unique_actions:offsite_conversion.fb_pixel_add_to_cart', 'cost_per_action_type:link_click', 'outbound_clicks_ctr:outbound_click', 'frequency', 'engagement_rate_ranking', 'cost_per_action_type:omni_add_to_cart', 'unique_actions:omni_add_to_cart', 'inline_post_engagement', 'spend', 'unique_actions:page_engagement', 'unique_actions:omni_purchase', 'cost_per_unique_inline_link_click', 'action:omni_add_to_cart', 'inline_link_click_ctr', 'cost_per_inline_post_engagement', 'objective', 'unique_inline_link_click_ctr', 'instant_experience_outbound_clicks', 'cost_per_unique_click', 'cost_per_action_type:post', 'social_spend', 'cost_per_action_type:post_engagement', 'date_stop', 'cost_per_action_type:omni_purchase', 'cost_per_inline_link_click', 'unique_actions:link_click', 'action:landing_page_view', 'unique_actions:post_reaction','unique_ctr', 'instant_experience_clicks_to_open', 'action:offsite_conversion.custom.280669215754025', 'cost_per_action_type:offsite_conversion.custom.281094269070676', 'unique_actions:post', 'cost_per_unique_action_type:landing_page_view', 'cost_per_unique_action_type:post_engagement', 'action:post_reaction', 'cost_per_unique_outbound_click:outbound_click', 'cpc', 'cpm', 'impressions', 'cost_per_unique_action_type:link_click', 'cost_per_unique_action_type:omni_purchase', 'cpp', 'action:offsite_conversion.fb_pixel_purchase', 'conversion_rate_ranking', 'unique_actions:offsite_conversion.fb_pixel_purchase', 'ctr', 'cost_per_action_type:page_engagement', 'cost_per_action_type:offsite_conversion.fb_pixel_purchase', 'outbound_clicks:outbound_click', 'unique_clicks', 'unique_inline_link_clicks', 'action:omni_purchase', 'action:page_engagement', 'unique_link_clicks_ctr', 'action:offsite_conversion.custom.118660332158323', 'action:offsite_conversion.custom.281094269070676', 'clicks', 'cost_per_action_type:landing_page_view', 'unique_outbound_clicks:outbound_click', 'cost_per_unique_action_type:omni_add_to_cart', 'website_ctr:link_click', 'action:offsite_conversion.fb_pixel_add_to_cart', 'instant_experience_clicks_to_start', 'action:link_click', 'quality_ranking', 'cost_per_action_type:offsite_conversion.custom.280669215754025', 'cost_per_action_type:offsite_conversion.fb_pixel_add_to_cart']

    for x in range(1,8):
        date1=today-datetime.timedelta(days=x)
        date1=str(date1)
        arr=date1.split("-")
        year=arr[0]
        month=arr[1]
        params = {'time_range': {'since': date1, 'until': date1}}
        fields = [
            'account_name',
            'campaign_name',
            'campaign_id',
            'reach',
           
            'frequency',
            'impressions',
            'clicks',
            'cpm',
            'ctr',
            'spend',
            'actions',
            'canvas_avg_view_percent',
            'canvas_avg_view_time',
            'conversion_rate_ranking',
            'conversion_values',
            'conversions',
            'cost_per_action_type',
            'cost_per_conversion',
            'cost_per_estimated_ad_recallers',
            'cost_per_inline_link_click',
            'cost_per_inline_post_engagement',
            'cost_per_outbound_click',
            'cost_per_thruplay',
            'cost_per_unique_action_type',
            'cost_per_unique_click',
            'cost_per_unique_inline_link_click',
            'cost_per_unique_outbound_click',
            'cpc',
            'cpp',
            'engagement_rate_ranking',
            'estimated_ad_recall_rate',
            'estimated_ad_recallers',
            'full_view_impressions',
            'full_view_reach',
            'inline_link_click_ctr',
            'inline_link_clicks',
            'inline_post_engagement',
            'instant_experience_clicks_to_open',
            'instant_experience_clicks_to_start',
            'instant_experience_outbound_clicks',
            'mobile_app_purchase_roas',
            'objective',
            'outbound_clicks',
            'outbound_clicks_ctr',
            'place_page_name',
         
            'quality_ranking',
            'social_spend',
            'unique_actions',
            'unique_clicks',
            'unique_ctr',
            'unique_inline_link_click_ctr',
            'unique_inline_link_clicks',
            'unique_link_clicks_ctr',
            'unique_outbound_clicks',
            'unique_outbound_clicks_ctr',
            'video_30_sec_watched_actions',
            'video_avg_time_watched_actions',
            'video_p100_watched_actions',
            'video_p25_watched_actions',
            'video_p50_watched_actions',
            'video_p75_watched_actions',
            'video_p95_watched_actions',
            'video_play_actions',
            'video_play_curve_actions',
            'video_thruplay_watched_actions',
            'website_ctr',
        
        ]

      
        f=open("account_id","r")                            #importing the account id from external file
        acc=f.read()
        my_account = AdAccount(acc)
        campaignids = my_account.get_campaigns()
       
        list_d=[]
        l=[]
        y=0
        for i in range(len(campaignids)):
            
            try:
                c_id=campaignids[i]["id"]
                campaign = Campaign(c_id)
                camp_insights = campaign.get_insights(fields=fields,params=params)
                j=0
                
                dic_camp={}
                for item in camp_insights:     #converting to dictionary           
                            dic_camp = dict(item)
                            
               
                
                try:
                        for each_action in dic_camp["actions"]:
                            dic_camp["action:"+each_action['action_type']]=each_action['value']
                        del dic_camp["actions"]
                except KeyError:
                        continue 
                
                
                try:  
                        for each_action in dic_camp["cost_per_action_type"]:
                            dic_camp["cost_per_action_type:"+each_action['action_type']]=each_action['value']
                        del dic_camp["cost_per_action_type"]
                except KeyError:
                        continue 
                try:   
                        for each_action in dic_camp["cost_per_outbound_click"]:
                            dic_camp["cost_per_outbound_click:"+each_action['action_type']]=each_action['value']
                        del dic_camp["cost_per_outbound_click"]
                except KeyError:
                        continue   
                try: 
                        for each_action in dic_camp["cost_per_unique_action_type"]:
                            dic_camp["cost_per_unique_action_type:"+each_action['action_type']]=each_action['value']
                        del dic_camp["cost_per_unique_action_type"]
                except KeyError:
                        continue  
                try:  
                        for each_action in dic_camp["cost_per_unique_outbound_click"]:
                            dic_camp["cost_per_unique_outbound_click:"+each_action['action_type']]=each_action['value']
                        del dic_camp["cost_per_unique_outbound_click"]
                except KeyError:
                        continue   
                try: 
                        for each_action in dic_camp["outbound_clicks"]:
                            dic_camp["outbound_clicks:"+each_action['action_type']]=each_action['value']
                        del dic_camp["outbound_clicks"]
                except KeyError:
                        continue  
                try:  
                        for each_action in dic_camp["outbound_clicks_ctr"]:
                            dic_camp["outbound_clicks_ctr:"+each_action['action_type']]=each_action['value']
                        del dic_camp["outbound_clicks_ctr"]
                except KeyError:
                        continue   
                
                try: 
                        for each_action in dic_camp["unique_actions"]:
                            dic_camp["unique_actions:"+each_action['action_type']]=each_action['value']
                        del dic_camp["unique_actions"]
                except KeyError:
                        continue   
                try: 
                        for each_action in dic_camp["unique_outbound_clicks"]:
                            dic_camp["unique_outbound_clicks:"+each_action['action_type']]=each_action['value']
                        del dic_camp["unique_outbound_clicks"]
                except KeyError:
                        continue  
                try:  
                        for each_action in dic_camp["unique_outbound_clicks_ctr"]:
                            dic_camp["unique_outbound_clicks_ctr:"+each_action['action_type']]=each_action['value']
                        del dic_camp["unique_outbound_clicks_ctr"]
                except KeyError:
                        continue  
                try:  
                        for each_action in dic_camp["website_ctr"]:
                            dic_camp["website_ctr:"+each_action['action_type']]=each_action['value']
                        del dic_camp["website_ctr"]
                except KeyError:
                        continue
                
                list_d.append(dic_camp)

                
            except IndexError:
                    continue
        if list_d:
            filename1="FacebookAds/landing_campaign_insights/"+"campaign_insights_"+date1+".csv"
            filename2="FacebookAds/processing_campaign_insights/csv/"+year+"/"+month+"/"+"campaign_insights_"+date1+".csv"
            importtos3.write_to_s3(list_d,fields1,'paragon-datalake',filename1,filename2)
    return list_d
        
def lambda_handler(event,context):  
    list1=campaign_insights()
    
    
    
    return {
        'statusCode':200
    }

