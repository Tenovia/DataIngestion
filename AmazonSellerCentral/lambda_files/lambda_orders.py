#Order Reports and Order Tracking Reports(yet to be specified)


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
def Unshipped_Orders_Report(yesterday,tomorrow):
    d=mws.get_report_request_list(MaxCount=2,ReportTypeList=['_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
    data=""
    for i in d.GetReportRequestListResult.ReportRequestInfo:

        if(i.ReportType!="FeedSummaryReport"):
            reportid=str(i.GeneratedReportId)
            report = mws.get_report(ReportId=reportid)
    
            #print report
            data+=report
    date = datetime.date.today()
    date=str(date)
    datelist=date.split('-')
    address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
  
    importtos3.write_to_s3(data,'paragon-datalake',address+'Unshipped_Orders_Report'+date+'.csv')        

def Flat_File_Orders_By_Order_Date_Report(yesterday,tomorrow):
    d=mws.get_report_list(MaxCount=1,ReportTypeList=['_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'],AvailableFromDate=yesterday+'T14:32:16.50-07',AvailableToDate=tomorrow+'T14:32:16.50-07')  
    
    
    #print d
    data=""
    for i in d.GetReportListResult.ReportInfo:
        #print "----------------",i.ReportType,i.ReportId,"-------------------------"
	

        if(i.ReportType!="FeedSummaryReport"):
            reportid=str(i.ReportId)
            report = mws.get_report(ReportId=reportid)
            data+=report
    date = datetime.date.today()
    date=str(date)
    datelist=date.split('-')
    address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
    importtos3.write_to_s3(data,'paragon-datalake',address+'Flat_File_Orders_By_Order_Date_Report'+date+'.csv') 
def main():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days = 1))
    tomorrow = str(today + datetime.timedelta(days = 1))
    today=str(today)
    d=mws.request_report(ReportType='_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_',StartDate=yesterday,EndDate=today)
    d=mws.request_report(ReportType='_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_',StartDate=yesterday,EndDate=today)

    Unshipped_Orders_Report(yesterday,tomorrow)
   
    Flat_File_Orders_By_Order_Date_Report(yesterday,tomorrow)
main()


def lambda_handler(context,switch):
    main()
    print "success"
