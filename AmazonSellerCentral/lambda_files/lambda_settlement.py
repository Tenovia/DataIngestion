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

def Flat_File_Settlement_Report(yesterday,tomorrow):
    

    d=mws.get_report_list(MaxCount=1,ReportTypeList=['_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_'],AvailableFromDate=yesterday+'T14:32:16.50-07',AvailableToDate=tomorrow+'T14:32:16.50-07')

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
    importtos3.write_to_s3(data,'paragon-datalake',address+"Flat_File_Settlement_Report"+date+".csv")

  
def main():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days = 1))
    tomorrow = str(today + datetime.timedelta(days = 1))
    today=str(today)

    Flat_File_Settlement_Report(yesterday,tomorrow)
    
main()

def lambda_handler(context,switch):
    main()
    print "success"
