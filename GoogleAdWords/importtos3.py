import boto3
import json
def write_to_s3(data, bucket_name, file_name, entry_per_line=False):
	s3 = boto3.resource("s3")
	s = ''
	if entry_per_line:
		for item in data:
			#s += json.dumps(item) + "\n"
			s+=item
	else:
		#s = json.dumps(data, indent=4, sort_keys=True)
		s=data
	s3.Bucket(bucket_name).put_object(Key=file_name, Body=s)
