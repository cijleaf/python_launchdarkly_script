!/usr/bin/env python 
# Description: 
#    Thsi script archives the directories storing the db files. 
# Parameters: None
# Author: 
# Create Date: 
# Updated By: 
# Updated Date
# Change Log 

import boto3
from botocore.exceptions import ClientError
from config import config

params = config('.database.ini')
vars = params['vars']

try:
   s3 = boto3.resource('s3')
   source = {'Bucket' : vars['processingdir'],
             'Key': vars['cstflnameproc'] + '.csv'}
   dest = s3.Bucket(vars['archivebucket'])
   dest.copy(source, vars['cstflnamearch'] + '.csv')
   print "Cost file was successfully copied to processing directory"

   source = {'Bucket' : vars['processingdir'],
            'Key' : vars['prdcrfrqncyflnameproc'] + '.csv'}
   dest = s3.Bucket(vars['archivebucket'])
   dest.copy(source, vars['prdcrfrqncyflnamearch'] + '.csv')
   print "Procedure Frequency file was successfully copied to processing directory"

   source = {'Bucket' : vars['processingdir'],
             'Key' : vars['mstrdescflnameproc'] + '.csv'}
   dest = s3.Bucket(vars['archivebucket'])
   dest.copy(source, vars['mstrdescflnamearch'] + '.csv')
   print "MVP Codeset file was successfully copied to processing directory"

   obj = s3.Object(vars['processingdir'], vars['cstflnameproc'] + '.csv')
   print("Cost file was successfully deleted from source directory")
   obj.delete() 

   obj = s3.Object(vars['processingdir'], vars['prdcrfrqncyflnameproc'] + '.csv') 
   print("Procedure Frequency file was successfully deleted from source directory.") 
   obj.delete() 

   obj = s3.Object(vars['processingdir'], vars['mstrdescflnameproc'] + '.csv') 
   print("MVP Codeset file was successfully deleted from source directory") 
   obj.delete()
 
except Exception as e:
       print ("File transfer was not successful") 
       print(e)
