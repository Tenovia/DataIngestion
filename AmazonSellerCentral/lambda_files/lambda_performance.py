from boto.mws.connection import MWSConnection 
import csv 
import cred
import importtos3
import datetime
MarketPlaceID = cred.marketplaceid()
MerchantID = cred.merchantid()
AccessKeyID = cred.accessid()
SecretKey = cred.secretkey()



mws = MWSConnection(AccessKeyID,SecretKey)

mws.SellerId = MerchantID
mws.Merchant = MerchantID
mws.MarketplaceId = MarketPlaceID
def Flat_File_Feedback_Report(yesterday,tomorrow):

	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_SELLER_FEEDBACK_DATA_'])#,RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	data=""
	#print d
	
	for i in d.GetReportRequestListResult.ReportRequestInfo:

       		reportid=str(i.GeneratedReportId)
       		report = mws.get_report(ReportId=reportid)
 
       		#print report
       		data+=report
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
        address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_performance"+date+".csv")
	
def main():
	today = datetime.date.today()
	yesterday = str(today - datetime.timedelta(days = 365))
	tomorrow = str(today + datetime.timedelta(days = 1))
	today=str(today)
	d=mws.request_report(ReportType='_GET_SELLER_FEEDBACK_DATA_',StartDate=yesterday,EndDate=today)

	Flat_File_Feedback_Report(yesterday,tomorrow)
main()
def lambda_handler(context,switch):
    main()
    print "success"
