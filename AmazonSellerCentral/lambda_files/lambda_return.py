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
def XML_Returns_Report_by_Return_Date(yesterday,tomorrow):
    dic={}
    d=mws.get_report_list(MaxCount=1,ReportTypeList=['_GET_XML_RETURNS_DATA_BY_RETURN_DATE_'],AvailableFromDate=yesterday+'T14:32:16.50-07',AvailableToDate=tomorrow+'T14:32:16.50-07')
    data=""
    #print d
    k=0
    for i in d.GetReportListResult.ReportInfo:
        #print "----------------",i.ReportType,i.ReportId,"-------------------------"


        if(i.ReportType!="FeedSummaryReport"):
            reportid=str(i.ReportId)
            report = mws.get_report(ReportId=reportid)
            
            rep=str(report)
            
            data+=rep
    date = datetime.date.today()
    date=str(date)
    datelist=date.split('-')
    address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
    importtos3.write_to_s3(data,'paragon-datalake',address+"XML_Returns_Report_by_Return_Date"+date+".csv")

def Flat_File_Returns_Report_by_Return_Date(yesterday,tomorrow):

    d=mws.get_report_list(MaxCount=1,ReportTypeList=['_GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE_'],AvailableFromDate=yesterday+'T14:32:16.50-07',AvailableToDate=tomorrow+'T14:32:16.50-07')
    data=""
    #print d
    for i in d.GetReportListResult.ReportInfo:
        #print "----------------",i.ReportType,i.ReportId,"-------------------------"


        if(i.ReportType!="FeedSummaryReport"):
            reportid=str(i.ReportId)
            report = mws.get_report(ReportId=reportid)
    
            #print report
            rep=str(report)
            data+=rep
    date = datetime.date.today()
    date=str(date)
    datelist=date.split('-')
    address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
    importtos3.write_to_s3(data,'paragon-datalake',address+"Flat_File_Returns_Report_by_Return_Date"+date+".csv")

            
def main():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days = 1))
    tomorrow = str(today + datetime.timedelta(days = 1))
    today=str(today)
    d=mws.request_report(ReportType='_GET_XML_RETURNS_DATA_BY_RETURN_DATE_',StartDate=yesterday,EndDate=today)
    d=mws.request_report(ReportType='_GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE_',StartDate=yesterday,EndDate=today)
	
    XML_Returns_Report_by_Return_Date(yesterday,tomorrow)            
    Flat_File_Returns_Report_by_Return_Date(yesterday,tomorrow)
main()

def lambda_handler(context,switch):
    main()
    print "success"
