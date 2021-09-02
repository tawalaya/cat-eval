#! /usr/env python3

import requests
import json
import os
from datetime import datetime
import time
import csv
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor

def aws_change_mem(function_name,mem):
     subprocess.check_call(["aws","lambda","update-function-configuration","--function-name",function_name, "--memory",str(mem)])

def gcf_change_mem(function_name,mem):
    subprocess.check_call(["gcloud","functions","deploy",function_name,"--memory",str(mem)])

def test_change_mem(function_name,mem):
    return

def main(fname,function_name="prime",changer=gcf_change_mem):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(execute(fname,function_name,changer))
    loop.run_until_complete(future)

async def execute(fname,function_name="prime",changer=gcf_change_mem):
    mandetory_keys = set(['name','url','inputs','itterations','memory'])
    if not os.path.isfile(fname):
        print("did not find",fname)
        return
    
    with open(fname,"r") as f:
        workload = json.load(f)
        for m in mandetory_keys:
            if not m in workload.keys():
                print(workload.keys(),"missing mandetory keys",m)
    
    oname = "data/{}_{}.csv".format(workload["name"],datetime.today().strftime('%Y-%m-%d'))
    with open(oname,"w") as f:
        fieldnames=["rStart","rEnd","status","mem","rLat","rId","eStart","eEnd","eLat","cId","cStart","vmId","osType","nodeVersion","pName","vName","cName","version","result","primeNumber","size","fname","platfrom","region","runtime","HID"]
        out = csv.DictWriter(f,fieldnames)
        out.writeheader()
        for mem in workload["memory"]:
            changer(function_name,mem)
            print("running",mem,":")
            for i in range(workload["itterations"]):
                with ThreadPoolExecutor(max_workers=4) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = [
                        loop.run_in_executor(
                            executor,
                            call,
                            *(workload["url"],workload["name"],mem,i,p) # Allows us to pass in multiple arguments to `fetch`
                        )
                        for p in workload["inputs"]
                    ]

                    for data in await asyncio.gather(*tasks):
                        out.writerow({key: value for key,value in data.items() if key in fieldnames})
                        time.sleep(0.5) 
            print()

                
def call(url,name,mem,itteration,inp):
    rid = "{}_{}".format(name,itteration)
    body = {
        "rId":rid,
        "prime":inp,
    }
    rStart=time.time()
    status = 400
    try:
        resp = requests.post(url,json=body,timeout=10)
        status = resp.status_code
        print("+",sep="")
    except requests.Timeout as e:
        status = 400
        print("-",sep="")

    rEnd=time.time()
    
    data = {}
    if status == 200:
        data = resp.json()
    else:
        data["rId"] = ""
        data["eStart"] = 0
        data["eEnd"] = 0
        data["eLat"] = -1
        data["cId"] = "None"
        data["cStart"] = 0
        data["vmId"] = "None"
        data["osType"] = "None"
        data["nodeVersion"] = "None"
        data["pName"] = "None"
        data["vName"] = "None"
        data["cName"] = "None"
        data["version"] = "None"
    data["rStart"]=rStart*1000
    data["rEnd"]=rEnd*1000
    data["status"]=status
    data["mem"]=mem
    data["rLat"]=(rEnd-rStart)
    return data


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    fname = None
    if len(args) > 0:
        fname = args[0]
        
    mode = "gcf"
    if len(args) > 1:
        mode = args[1]
        
    funcName = "prime"
    if len(args) > 2:
        funcName = args[2]
    
    if fname is None:
        print("need workload file as first param")
        sys.exit(0)

    if mode == "gcf":
        main(fname,funcName,gcf_change_mem)
    elif mode == "aws":
        main(fname,funcName,aws_change_mem)
    elif mode == "test":
        main(fname,funcName,test_change_mem)
    else:
        print("unknown mode!")


        
        

