import json

MAX_INT = 99999999

class Analyzer:

    def __init__(self):
        pass

    def insert_port_time(self, min_time_each_port, port, time):
        if port in min_time_each_port:
            if time < min_time_each_port[port]:
                min_time_each_port[port] = time
        else:
            min_time_each_port[port] = time


    def analyze_one_scanning_type(self, data):

        success_attack_num = 0
        all_experiment_min_times = []
        min_time_each_port = {}

        for one_command_result in data.get("result"): ###
            if len(one_command_result) != 0:
                success_attack_num += 1
            one_command_min_time = MAX_INT  


            for found_host in one_command_result: ###
                time = found_host.get("time")
                if time < one_command_min_time:
                    one_command_min_time = time

                for port in found_host.get("ports"): ###
                    self.insert_port_time(min_time_each_port, port, time)
            
            if one_command_min_time != MAX_INT:
                all_experiment_min_times.append(one_command_min_time)

        scanning_mean_min_of_all = self.calc_min_of_all(all_experiment_min_times)
        scanning_mean_min_each_port = self.calc_scanning_mean_min_each_port(min_time_each_port)
        scanning_success_probability = success_attack_num/data.get("count")
        return scanning_success_probability, scanning_mean_min_of_all, scanning_mean_min_each_port
    
    def calc_min_of_all(self, all_experiment_min_times):
        if len(all_experiment_min_times) == 0:
            scanning_mean_time = None
        else:
            scanning_mean_time = sum(all_experiment_min_times)/len(all_experiment_min_times)
        return scanning_mean_time
    
    def calc_scanning_mean_min_each_port(self, min_time_each_port):
        scanning_min_times = list(min_time_each_port.values())
        if len(scanning_min_times) == 0:
            return None
        else:
            return sum(scanning_min_times)/len(scanning_min_times)

    def get_keys(self, match, analyze_result):
        matches = match.split("_")
        keys = []
        for key in analyze_result:
            key_pieces = key.split("_")
            if key_pieces[-1] == matches[-1] and\
                key_pieces[-2] == matches[-2]:
                keys.append(key)
        return keys
    
    def print_line(self, key, analyze_result):
        time = key.split("_")[1]
        print("{} ASP:{} AMT:{}".format(
            time, 
            analyze_result.get(key).get("scanning_success_probability"),
            analyze_result.get(key).get("scanning_mean_time")))

    def visualize(self, analyze_result):
        print("\nscan type: -sU(UDP scanning) Scanning port range 1-9000")
        keys = self.get_keys("ScansU_Port1-9000", analyze_result)
        for key in keys:
            self.print_line(key, analyze_result)
        
        print("\nscan type: -sT(TCP connect scanning) Scanning port range 1-9000")
        keys = self.get_keys("ScansT_Port1-9000", analyze_result)
        for key in keys:
            self.print_line(key, analyze_result)

        print("\nscan type: -sS(TCP SYN scanning) Scanning port range 1-9000")
        keys = self.get_keys("ScansS_Port1-9000", analyze_result)
        for key in keys:
            self.print_line(key, analyze_result)
        
        print("\nscan type: -sS(TCP SYN scanning) Scanning specified ports")
        keys = self.get_keys("ScansS_Portdiscovered", analyze_result)
        for key in keys:
            self.print_line(key, analyze_result)



    def run(self, nmap_result, file_name):
        analyze_result = {}
        for key in nmap_result:
            data = nmap_result.get(key)
            scanning_success_probability, scanning_mean_min_of_all, scanning_mean_min_each_port = self.analyze_one_scanning_type(data)
            analyze_result[key] = {
                "scanning_success_probability":scanning_success_probability,
                "scanning_mean_min_of_all":scanning_mean_min_of_all,
                "scanning_mean_min_each_port":scanning_mean_min_each_port,
            }
        print(json.dumps(analyze_result, indent=4))
        with open(file_name, "w") as f:
            f.write(json.dumps(analyze_result, indent=4))
        self.visualize(analyze_result)


