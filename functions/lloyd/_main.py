import random
import json
from logging import start, end

def randomOpt(left, right):
    a = left[random.randint(0, len(left) - 1)]
    b = right[random.randint(0, len(right) - 1)]

    c = 0
    if random.uniform(0, 1) < 0.5:
        c = a * b
    else:
        if b > 0:
            c = a / b
        else:
            c = a * b

    if random.uniform(0, 1) < 0.5:
        left[random.randint(0, len(left) - 1)] = c
    else:
        right[random.randint(0, len(right) - 1)] = c

    return left, right


def compute(i, anchor, left, right):
    if i < anchor:
        compute(i + 1, anchor, left, right)
    else:
        randomOpt(left, right)


def generateOperatorArray(n):
    data = []
    for i in range(n):
        data.append(random.uniform(0.1, 9.9) * random.randint(1, 10000))
    return data


def Memory(task):

    if not all(k in task for k in ("operator_size", "iterations", "recursion_depth")):
        task["operator_size"] = $OPSIZE
        task["iterations"]    = $ITTER
        task["recursion_depth"] = $DEPTH

    left = generateOperatorArray(task["operator_size"])
    right = generateOperatorArray(task["operator_size"])
    for i in range(task["iterations"]):
        compute(0, task["recursion_depth"], left, right)
        if i % 100 == 0:
            tmp = left.copy()
            left = right.copy()
            right = tmp

    return left, right


def lambda_handler(event, context):
    start()
    l,r = Memory(event)
    data =end({"size":(len(l)+len(r))})
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response

def gcf_handler(request):
    event = request.get_json()
    if event:
        start()
        l,r = Memory(event)
        data = end({"size":(len(l)+len(r))})

        return json.dumps(data), 200, {'ContentType': 'application/json'}
    else:
        return "{\"message\":\"unknown body\"}", 400, {'ContentType': 'application/json'}
