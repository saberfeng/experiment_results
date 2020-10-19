import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import json
from os import listdir, walk
from os.path import isfile, join

# {
#     "address":"10.0.0.1",
#     "ports":[21,22],
#     "time":10,
# }

def get_host_ports(host):
    port_list = []
    ports = host.find("ports")
    for port in ports.findall("port"):
        state = port.find("state")
        if state.get("state") == "open":
            port_list.append(int(port.get("portid")))
    return port_list

def get_host_address(host):
    for address in host.findall("address"):
        if address.get("addrtype") == "ipv4":
            return address.get("addr")

def get_host_time(host):
    return int(host.get("endtime")) - int(host.get("starttime"))

def parse_host(host):
    parsed_host = {}
    address = get_host_address(host)
    port_list = get_host_ports(host)
    time = get_host_time(host)
    if len(port_list) != 0 and address: 
        parsed_host["ports"] = port_list
        parsed_host["address"] = address
        parsed_host["time"] = time        
    return parsed_host

def parse_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    # print(root.tag)
    result = []
    for host in root.findall("host"):
        parsed_host = parse_host(host)
        if parsed_host:
            result.append(parsed_host)
    return result

def parse_files(file_list):
    pass

def get_scan_type_key(file_path):
    # files = [f for f in listdir(directory)]
    # if len(files) == 0:
    #     raise Exception("No files in directory:"+directory)
    # else:
    #     filename = files[0]
    # "./FRVM_100s/nmap_Time100_ScansS_Portdiscovered_399.xml"
    file_name = file_path.split("/")[-1]
    key_segments = file_name[:-4].split("_")[:-1]
    return "_".join(key_segments)

# {
#     "nmap_Time100_ScansS_Port1-9000":{
#         "count":700,
#         "result":[
#             [
#                 {
#                     "address":"10.0.0.1",
#                     "ports":[21,22],
#                     "time":10,
#                 },
#                 {
#                     "address":"10.0.0.12",
#                     "ports":[21,22],
#                     "time":10,
#                 },
#             ],
#             [
#                 {
#                     "address":"10.0.0.12",
#                     "ports":[21,22],
#                     "time":10,
#                 },
#             ],
#         ]
#     }
# }

def insert_file_scan_result(total_result, key, file_scan_result):
    if key in total_result:
        total_result[key]["result"].append(file_scan_result)
    else:
        total_result[key] = {
            "count":0,
            "result":[file_scan_result],
        }

def increment_count(total_result, key):
    if key in total_result:
        total_result[key]["count"] += 1
    else:
        total_result[key] = {
            "count":1,
            "result":[],
        }

def parse(mode, paths):
    if mode == "files":
        for path in paths:
            result = parse_file(path)
            print(json.dumps(result, indent=4))
    if mode == "dirs":
        total_result = {}
        for directory in paths:
            for file_path in [join(directory,f) for f in listdir(directory)]:
                key = get_scan_type_key(file_path)
                increment_count(total_result, key)
                try:
                    file_result = parse_file(file_path)
                except ParseError as e:
                    continue
                insert_file_scan_result(total_result, key, file_result)
    with open("output", "w") as f:
        f.write(json.dumps(total_result, indent=4))


if __name__ == "__main__":
    param1 = {
        "mode":"files",
        "paths":["./FRVM_100s/nmap_Time100_ScansS_Portdiscovered_399.xml"],
    }
    param2 = {
        "mode":"dirs",
        "paths":["./FRVM_100s", "./FRVM_200s", "./FRVM_300s", "./FRVM_400s", "./FRVM_500s"],
    }
    parse(**param2)
    # print(get_scan_type_key("./FRVM_100s/nmap_Time100_ScansS_Portdiscovered_399.xml"))