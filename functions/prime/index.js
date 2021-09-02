'use strict';

const fs = require('fs');
const logger = require("./logging")
const prime = require("./prime")

function logic(num,id) {
    var number;
    if (num != undefined && typeof num == 'number'){
        number = num;
    } else {
        number = Math.floor((Math.random() * 1000) + 7500000)
    }
    logger.start(id);
    var result = prime(number);
    return logger.end(number,result);
}

//gcf-hook
exports.http = (request, response) => {
    var num = undefined;
    var rId = undefined;
    if (request.body != undefined){
        num = request.body.prime;
        rId = request.body.rId;
    }
    if (rId == undefined || rId == "") {
        rId = (Date.now()+Math.floor(Math.random() * 10000000)).toString(32).toUpperCase();
    }

    response.status(200).send(logic(num,rId))
};

//aws hook
exports.aws = async (event, context) => {
    try {
        console.log(event.body);
        var num = undefined;
        var rId = undefined;
        if (event.body != undefined){
            num = event.body.prime;
            rId = event.body.rId;
        }
        if (rId == undefined || rId == "") {
            rId = (Date.now()+Math.floor(Math.random() * 10000000)).toString(32).toUpperCase();
        }
        const result = logic(num,rId);
        
        return {
            statusCode: 200,
            body: JSON.stringify(result),
        };
    } catch (e) {
        console.log(e);
        return {
            statusCode: 400,
            body: JSON.stringify(e),
        };
    }
};
