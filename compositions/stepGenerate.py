#! /usr/bin/env python

import json
import subprocess


def deploy(function_config):
    export_vars=[]
    for k in function_config["params"].keys():
        export_vars.append(f"{k}={function_config['params'][k]}")


    subprocess.check_call(export_vars+["make","AWS"],cwd=f"../functions/{function_config['type']}")
    aws_function = subprocess.check_output(["aws","lambda","get_function","--function-name",function_config["name"]])
    data = json.loads(aws_function)
    function_config["arn"] = data["FunctionArn"]
    return data["FunctionArn"]

def generate(config,sf=1,deploy=False):
    if deploy:
        for function_config in config["functions"]:
            deploy(function_config)
    

    functions = {}
    for function_config in config["functions"]:
        if "arn" in function_config:
            functions[function_config["name"]] = function_config["arn"]
        else:
              functions[function_config["name"]] = "not set"

    stepFunction = {
        "Comment":f"{config['name']}_{sf}",
        "StartAt":"F1",
    }

    if len(config["flow"]) <= 0:
        print("flow was not defined correctly, did nothing")
        return
    
    counter = 1
    last = None
    def add_task(p,counter):
        states[f"F{counter}"] = {
                "Type": "Task",
                #get the arn of the referenced function
                "Resource": f"{functions[p['function']]}",
                "InputPath": f"$.f{counter}",
                "ResultPath": f"$.f{counter}_result",
                "Next":f"F{counter+1}"
        }

    def add_ptask(p,branch,counter):
        branch.append({
          "StartAt": f"F{counter}",
          "States": {
            f"F{counter}": {
              "Type": "Task",
              "InputPath": f"$.f{counter}",
              "ResultPath": f"$.f{counter}_result",
              "Resource": f"{functions[p['function']]}",
              "End": True
            }
          }
        })



    states = {}
    for p in config["flow"]:
        #add a normal task
        if type(p) is dict:
            repeat = eval(p["repeat"])
            if repeat >= 1:
                for i in range(repeat):
                    add_task(p,counter)
                    last=f"F{counter}"
                    counter+=1
        elif type(p) is list:
            start = counter
            counter+=1
            branches = []
            for x in p:
                repeat = eval(x["repeat"])
                if repeat >= 1:
                    for i in range(repeat):
                        add_ptask(x,branches,counter)
                        counter+=1
            states[f"F{start}"] = {
                "Type": "Parallel",
                "ResultPath": f"$.f{start}_result",
                "Branches":branches,
                "Next":f"F{counter}"
            }
            last=f"F{start}"

    #fix end..        
    del states[last]["Next"]
    states[last]["End"]=True
    stepFunction["States"] = states

    print(json.dumps(stepFunction))
            
if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if len(args) <= 0:
        print("missing config file!")
    config_file = args[0]

    sf = 0
    if len(args) >= 2:
        sf = int(args[1])

    deploy = False
    if len(args) >= 3:
        deploy = True
    
    with open(config_file,'r') as f:
        config = json.load(f)
        generate(config,sf,deploy)