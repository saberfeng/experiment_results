from nmap_parser import parse
from analyzer import Analyzer
from visualizer import Visualizer
import json


def read_json(file_name):
    with open(file_name, "r") as f:
        return json.loads(f.read())

def run():
    FRVM_result = {}
    simple_swtich_result = {}

    #----------parsing-------------------------
    param2 = {
        "mode":"dirs",
        "paths":["./FRVM_100s", "./FRVM_200s", "./FRVM_300s", "./FRVM_400s", "./FRVM_500s"],
        "output_filename":"./parse_analysis_result/parsed_FRVM.json",
    }
    FRVM_result = parse(**param2)

    param3 = {
        "mode":"dirs",
        "paths":["./simple_switch_100s", "./simple_switch_200s", "./simple_switch_300s", "./simple_switch_400s", "./simple_switch_500s"],
        "output_filename":"./parse_analysis_result/parsed_tSDN.json",
    }
    simple_swtich_result = parse(**param3)
    #--------------------------------------------

    if not FRVM_result or not simple_swtich_result:
        FRVM_result = read_json("./parse_analysis_result/FRVM_parsed.json")
        simple_swtich_result = read_json("./parse_analysis_result/simple_switch_parsed.json")
    
    #-----------analyzing-----------------------
    analyzer = Analyzer()
    analyzer.run(FRVM_result, "./parse_analysis_result/analyzed_FRVM.json")
    analyzer.run(simple_swtich_result, "./parse_analysis_result/analyzed_tSDN.json")

    #-----------visualize-----------------------
    visualizer = Visualizer()


if __name__ == "__main__":
    run()