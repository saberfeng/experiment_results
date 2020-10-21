import json

class Analyzer:

    def __init__(self):
        pass

    def analyze_one_scanning_type(self, data):
        success_attack_num = 0
        scanning_total_time = []

        for one_command_result in data.get("result"):
            if len(one_command_result) != 0:
                success_attack_num += 1
            for found_host in one_command_result:
                scanning_total_time.append(found_host.get("time"))
        if len(scanning_total_time) == 0:
            scanning_mean_time = None
        else:
            scanning_mean_time = sum(scanning_total_time)/len(scanning_total_time)
        scanning_success_probability = success_attack_num/data.get("count")
        return scanning_success_probability, scanning_mean_time

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



    def run(self, nmap_result):
        analyze_result = {}
        for key in nmap_result:
            data = nmap_result.get(key)
            scanning_success_probability, scanning_mean_time = self.analyze_one_scanning_type(data)
            analyze_result[key] = {
                "scanning_success_probability":scanning_success_probability,
                "scanning_mean_time":scanning_mean_time,
            }
        print(json.dumps(analyze_result, indent=4))
        with open("./analyze_result.json", "w") as f:
            f.write(json.dumps(analyze_result, indent=4))
        self.visualize(analyze_result)


