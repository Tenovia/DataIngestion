import campaign_insights
import country_region
import age_gender
import device
import publisher_platform


def lambda_handler(event,context):  
    list1=campaign_insights.campaign_insights()
    list2=country_region.country_region()
    list3=age_gender.age_gender()
    list4=device.device()
    list5=publisher_platform.publisher_platform()

    
    
    return {
        'statusCode':200
    }