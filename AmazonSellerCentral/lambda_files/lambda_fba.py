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

def FBA_Amazon_Fulfilled_Shipments_Report(yesterday,tomorrow):
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	#print d											
	data=""								#.GetReportRequestListResult.ReportRequestInfo[0]
	for i in d.GetReportRequestListResult.ReportRequestInfo:
		if i.ReportProcessingStatus == '_DONE_NO_DATA_':
			data+= "No data present for the request\n"
			continue

        	reportid=str(i.GeneratedReportId)
        	report = mws.get_report(ReportId=reportid)
		data+=report 
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
        #address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
	address='amazonsellercentral/landing/fba/'
	importtos3.write_to_s3(data,'paragon-datalake',address+'FBA_Amazon_Fulfilled_Shipments_Report'+date+'.csv')
	
	
def Flat_File_All_Orders_Report_by_Order_Date(yesterday,tomorrow):

	
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	#print d	
	data=""
	for i in d.GetReportRequestListResult.ReportRequestInfo:

       		reportid=str(i.GeneratedReportId)
       		report = mws.get_report(ReportId=reportid)
 
       		#print report
       		data+=report
	print data

        address='amazonSellerCentral/landing/fba/'
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_performance.csv")
	#print "success"
    
def FBA_Amazon_Fulfilled_Inventory_Report(yesterday,tomorrow):

	
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_AFN_INVENTORY_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	#print d                                                                                          #,"\n",d2	
	data=""
	for i in d.GetReportRequestListResult.ReportRequestInfo:
		if i.ReportProcessingStatus == '_DONE_NO_DATA_':
			data+="No data present for the request"
			continue	
    		#print "----------------",i.ReportType,i.GeneratedReportId,"-------------------------"

    
        	reportid=str(i.GeneratedReportId)
        	report = mws.get_report(ReportId=reportid)
		data+=report  
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
    #address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
	address='amazonsellercentral/landing/fba/'	
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_FBA_fulfilled_Inventory"+date+".csv")
	
    
def FBA_Reimbursements_Report(yesterday,tomorrow):
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_FBA_REIMBURSEMENTS_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	data=""                                                                                         #,"\n",d2	

	for i in d.GetReportRequestListResult.ReportRequestInfo:	
    		
		if i.ReportProcessingStatus == '_DONE_NO_DATA_':
			data+= "No data present for the request"
			continue
			
    		#print "----------------",i.ReportType,i.GeneratedReportId,"-------------------------"


    
        	reportid=str(i.GeneratedReportId)
        	report = mws.get_report(ReportId=reportid)
		data+=report 
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
        #address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
	address='amazonsellercentral/landing/fba/'	
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_FBA_Reimbursements_REPORT"+date+".csv")

def FBA_Returns_Report(yesterday,tomorrow):
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	                                                                                        #,"\n",d2	
	data=""
	for i in d.GetReportRequestListResult.ReportRequestInfo:	
    		#print "----------------",i.ReportType,i.GeneratedReportId,"-------------------------"
        	reportid=str(i.GeneratedReportId)
        	report = mws.get_report(ReportId=reportid)
		data+=report  
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
    #address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'        
	address='amazonsellercentral/landing/fba/'
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_FBA_RETURNS_REPORT"+date+".csv")

def FBA_Replacements_Report(yesterday,tomorrow):
	d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_REPLACEMENT_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
	                                                                                        #,"\n",d2	
	data=""
	for i in d.GetReportRequestListResult.ReportRequestInfo:	
		#print "----------------",i.ReportType,i.GeneratedReportId,"-------------------------"
		reportid=str(i.GeneratedReportId)
		report = mws.get_report(ReportId=reportid)
		data+=report
        date = datetime.date.today()
        date=str(date)
        datelist=date.split('-')
        #address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
	address='amazonsellercentral/landing/fba/'	
	importtos3.write_to_s3(data,'paragon-datalake',address+"mws_FBA_REPLACEMENTS_REPORT"+date+".csv")
	


def main():
	today = datetime.date.today()
	yesterday = str(today - datetime.timedelta(days = 10))
	tomorrow = str(today + datetime.timedelta(days = 1))
	today=str(today)
	#d=mws.request_report(ReportType='_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_',StartDate=yesterday,EndDate=today)
	d=mws.request_report(ReportType='_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_',StartDate=yesterday,EndDate=today)
	#d=mws.request_report(ReportType='_GET_AFN_INVENTORY_DATA_',StartDate=yesterday,EndDate=today)
	#d=mws.request_report(ReportType='_GET_FBA_REIMBURSEMENTS_DATA_',StartDate=yesterday,EndDate=today)
	#d=mws.request_report(ReportType='_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_',StartDate=yesterday,EndDate=today)		
	#d=mws.request_report(ReportType='_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_REPLACEMENT_DATA_',StartDate=yesterday,EndDate=today)					 


	#FBA_Amazon_Fulfilled_Shipments_Report(yesterday,tomorrow)
	Flat_File_All_Orders_Report_by_Order_Date(yesterday,tomorrow)
	#FBA_Amazon_Fulfilled_Inventory_Report(yesterday,tomorrow)
	#FBA_Reimbursements_Report(yesterday,tomorrow)
	#FBA_Returns_Report(yesterday,tomorrow)
	#FBA_Replacements_Report(yesterday,tomorrow)

main()
def lambda_handler(context,switch):
    main()
    print "success"
        
	
