const fs = require('fs');
const os = require("os");

function hashString(str){
	let hash = 0;
	for (let i = 0; i < str.length; i++) {
		hash += Math.pow(str.charCodeAt(i) * 31, str.length - i);
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}

const cStart = Date.now()
const containerId = (cStart+Math.floor(Math.random() * 10000000)).toString(32).toUpperCase()
//Adapted from github.com/wlloyduw/SAAF
function faas_fingerprint(){
    var vmId = process.platform;
    if (vmId == "win32" || vmId == "win64") {
        
        vmId = process.env["COMPUTERNAME"]
    } else  {
        vmId =  Math.floor((Date.now()/1000)-(fs.readFileSync("/proc/uptime").toString().split(" ")[0].split(".")[0])).toString(32).toUpperCase();
    }
    let fingerprint = {};
    fingerprint["vId"] = vmId;
    var key = process.env.GOOGLE_CLOUD_PROJECT;
    if (key != null) {
        fingerprint["platform"] = "GCF";
        fingerprint["CId"] = containerId;
        fingerprint["region"] = process.env.FUNCTION_REGION;
        fingerprint["HId"] = vmId;
        fingerprint["extras"] = process.env.SUPERVISOR_HOSTNAME;
        fingerprint["version"] = "Unknown";
        fingerprint["memory"] = process.env.FUNCTION_MEMORY_MB; 
        fingerprint["RAW"] = fs.readFileSync("/proc/uptime").toString();
    } else if((key = process.env.FUNCTION_TARGET) != null) {
        fingerprint["platform"] = "GCF";
        fingerprint["CId"] = containerId;
        fingerprint["region"] = "Unknown";
        fingerprint["HId"] = vmId;
        fingerprint["extras"] = "Unknown";
        fingerprint["version"] = process.env.K_REVISION;
        fingerprint["memory"] = 0; 
        fingerprint["RAW"] = fs.readFileSync("/proc/uptime").toString();
    } else if((key = process.env.AWS_LAMBDA_LOG_STREAM_NAME) != null){
        fingerprint["platform"] = "AWS";
        fingerprint["CId"] = key;
        fingerprint["region"] = process.env.AWS_REGION;
        fingerprint["version"] = process.env.AWS_LAMBDA_FUNCTION_VERSION;
        fingerprint["memory"] = process.env.AWS_LAMBDA_FUNCTION_MEMORY_SIZE; 
        var vmID = fs.readFileSync("/proc/self/cgroup").toString();
        var index = vmID.indexOf("sandbox-root");
        fingerprint["HId"] = vmID.substring(index + 13, index + 19);
        fingerprint["RAW"] = vmID;
        fingerprint["extras"] = fs.readFileSync("/proc/uptime").toString();
    } else {
        fingerprint["platform"] = "Unknown";
        fingerprint["CId"] = containerId;
        fingerprint["HId"] = vmId;
        fingerprint["region"] = "Unknown";
        fingerprint["RAW"] = "Unknown";
        fingerprint["extras"] = "Unknown";
        fingerprint["version"] = "Unknown";
        fingerprint["memory"] = "Unknown"; 
    }

    return fingerprint;
}

//detect vm id based on either boot time or mac-address+hostname (should be VM unique in azure)
const fingerprint = faas_fingerprint();

const osType = process.platform
const nodeVersion = process.version


let startTime;
let rid;

module.exports.start = (id) => {
    startTime = Date.now()
    rid = id;
}
module.exports.end = (primeNumber,result) => {
    const eEnd = Date.now()
    return {
        rId:rid,
        eStart: startTime,
        eEnd,
        eLat: eEnd - startTime,
        cId:fingerprint["CId"],
        cStart,
        vmId:fingerprint["HId"],
        primeNumber,
        result,
        osType,
        nodeVersion,
        pName:fingerprint["platform"],
        vName:fingerprint["vId"],
        region:fingerprint["region"],
        cName:containerId,
        eMem:fingerprint["memory"],
        version:fingerprint["version"],
        raw:fingerprint["RAW"],
        extras:fingerprint["extras"],
    }
}
