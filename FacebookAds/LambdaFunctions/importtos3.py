import csv
import json
import boto3
def write_to_s3(list_d,fields1, bucket_name, file_name1, file_name2,entry_per_line=False):
  s3 = boto3.resource("s3")
  s = ''
  s1=''
  for names in fields1:
    s+=str(names)+","
  s=s[:-1]
  s+="\n"
  #print(s)
  k=0
  n=len(list_d)
  while(k<n):
    for name in fields1:
      try:
        if(name in list_d[k].keys()):
          s1+=(list_d[k][name])+","
        else:
          s1+="NULL"+","
      except KeyError:
        s1+="NULL"+","
    s1=s1[:-1]
    s1+="\n"
    k+=1
 
  #print(s1)
  s+=s1 
 
  s3.Bucket(bucket_name).put_object(Key=file_name1, Body=s)
  s3.Bucket(bucket_name).put_object(Key=file_name2, Body=s)




