from datetime import datetime
import random
import math
import sys
import os


FREEZER_OFFSET = len("freezer:/sandbox-")
def read_cgroup_ids(trace):
        try:
            file = open('/proc/self/cgroup', 'r')
            lines = file.readlines()
            found = 0
            for line in lines:
                index = line("freezer")
                if index > 0:
                    trace["freezer"] = line[index + FREEZER_OFFSET:].strip()
                    found += 1
                index = line.find("sandbox-root-")
                if index > 0:
                    line = line[index:]
                    if len(line) < 57:
                        raise ValueError
                    host = line[13:19]
                    trace["HID"] = host
                    trace.HostID = host
                    trace["service"] = line[36:42]
                    trace["sandbox"] = line[51:57]
                    found += 1
                if found >= 2:
                    break
        finally:
            return

def uptime():  
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

def id(t):
    return f"{int(((t.timestamp()*1000)+math.floor(random.uniform(0,1)* 10000000))):012x}"

cStart = datetime.now()
cId =  id(cStart)
osType = sys.platform
version = sys.version

startTime = cStart
rId = cId

def start():
    global startTime
    global rId
    startTime = datetime.now()
    rId = id(startTime)

def fingerprint():
    fingerprint = {}
    #selects provider based on env variables
    aws_key = os.getenv("AWS_LAMBDA_LOG_STREAM_NAME")
    gcf_key = os.getenv("X_GOOGLE_FUNCTION_NAME")
    ow_key = os.getenv("__OW_ACTION_NAME")
    acf_key = os.getenv("WEBSITE_HOSTNAME")

    fingerprint["platform"] = "unkonwn";
    fingerprint["cId"]      = cId;
    fingerprint["region"]   = "unkonwn";
    fingerprint["version"]  = "unkonwn";
    fingerprint["memory"]   = "unkonwn";
    fingerprint["extras"] = uptime()

    if aws_key:
        fingerprint["platform"] = "AWS";
        fingerprint["cId"]      = aws_key;
        fingerprint["region"]   = os.getenv("AWS_REGION");
        fingerprint["version"]  =  os.getenv("AWS_LAMBDA_FUNCTION_VERSION");
        fingerprint["memory"]   =  os.getenv("AWS_LAMBDA_FUNCTION_MEMORY_SIZE")
        
    elif gcf_key:
        fingerprint["platform"] = "GCF";
        fingerprint["region"]   = os.getenv("X_GOOGLE_FUNCTION_REGION");
        fingerprint["HId"]      = os.getenv("X_GOOGLE_SUPERVISOR_HOSTNAME");
        fingerprint["version"]  = os.getenv("K_REVISION");
        fingerprint["memory"]   = os.getenv("X_GOOGLE_FUNCTION_MEMORY_MB"); 
    
    read_cgroup_ids(fingerprint)

    return fingerprint


f = fingerprint()
def end(extras):
    end = datetime.now()  
    
    return {
        "rId":rId,
        "eStart": int(startTime.timestamp()*1000),
        "eEnd":int(end.timestamp()*1000),
        "eLat": int((end - startTime).total_seconds()*1000),
        "cStart":int(cStart.timestamp()*1000),
        "osType":osType,
        "runtime":version,
        "cName":cId,
    } | f | extras


