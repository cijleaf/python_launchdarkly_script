#!/usr/bin/env python 
# Description: 
#    This script moves the db files from ingestion bucket to S3 folder for processing. It also deletes files from# source directory. 
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

   #read config params 
   #params = config('.database.ini')
   #vars = params['vars']
   
   s3 = boto3.resource('s3')
   source = {'Bucket' : vars['sourcedatadir'],
             'Key': vars['cstflname'] + '.csv'}
   dest = s3.Bucket(vars['processingdir'])
   dest.copy(source, vars['cstflnameproc'] + '.csv')
   print "Cost file was successfully copied to processing directory"

   source = {'Bucket' : vars['sourcedatadir'],
            'Key' : vars['prdcrfrqncyflname'] + '.csv'}
   dest = s3.Bucket(vars['processingdir'])
   dest.copy(source, vars['prdcrfrqncyflnameproc'] + '.csv')
   print "Procedure Frequency file was successfully copied to processing directory"

   source = {'Bucket' : vars['sourcedatadir'],
             'Key' : vars['mstrdescflname'] + '.csv'}
   dest = s3.Bucket(vars['processingdir'])
   dest.copy(source, vars['mstrdescflnameproc'] + '.csv')
   print "MVP Codeset file was successfully copied to processing directory"

   obj = s3.Object(vars['sourcedatadir'], vars['cstflname'] + '.csv')
   print("Cost file was successfully deleted from source directory")
   obj.delete() 

   obj = s3.Object(vars['sourcedatadir'], vars['prdcrfrqncyflname'] + '.csv') 
   print("Procedure Frequency file was successfully deleted from source directory.") 
   obj.delete() 

   obj = s3.Object(vars['sourcedatadir'], vars['mstrdescflname'] + '.csv') 
   print("MVP Codeset file was successfully deleted from source directory") 
   obj.delete()
 
except Exception as e:
       print ("File transfer was not successful") 
       print(e)
