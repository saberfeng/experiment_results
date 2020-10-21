import matplotlib.pyplot as plt
import json

class Visualizer:

    def __init__(self):
        self.read_analysis_result()
        self.preprocess_data()
        self.keys_sS_Port1_9000 = [
            "nmap_Time100_ScansS_Port1-9000",
            "nmap_Time200_ScansS_Port1-9000",
            "nmap_Time300_ScansS_Port1-9000",
            "nmap_Time400_ScansS_Port1-9000",
            "nmap_Time500_ScansS_Port1-9000",
        ]
        self.keys_sT_Port1_9000 = [
            "nmap_Time100_ScansT_Port1-9000",
            "nmap_Time200_ScansT_Port1-9000",
            "nmap_Time300_ScansT_Port1-9000",
            "nmap_Time400_ScansT_Port1-9000",
            "nmap_Time500_ScansT_Port1-9000",
        ]
        self.keys_sU_Port1_9000 = [
            "nmap_Time100_ScansU_Port1-9000",
            "nmap_Time200_ScansU_Port1-9000",
            "nmap_Time300_ScansU_Port1-9000",
            "nmap_Time400_ScansU_Port1-9000",
            "nmap_Time500_ScansU_Port1-9000",
        ]
        self.keys_sS_Portdiscovered = [
            "nmap_Time100_ScansS_Portdiscovered",
            "nmap_Time200_ScansS_Portdiscovered",
            "nmap_Time300_ScansS_Portdiscovered",
            "nmap_Time400_ScansS_Portdiscovered",
            "nmap_Time500_ScansS_Portdiscovered",
        ]
        self.x_axis = [100,200,300,400,500]
        self.x_label = "MTD Interval (s)"
        self.y_label = {
            "scanning_success_probability":"Scanning Success Probability",
            "scanning_mean_min_of_all":"Scanning Mean Time (s)",
            "scanning_mean_min_each_port":"Scanning Mean Time (s)",
        }

    def read_analysis_result(self):
        analyzed_FRVM_filename = "./parse_analysis_result/analyzed_FRVM.json"
        analyzed_tSDN_filename = "./parse_analysis_result/analyzed_tSDN.json"
        self.analyzed_FRVM = self.read_json(analyzed_FRVM_filename)
        self.analyzed_tSDN = self.read_json(analyzed_tSDN_filename)
    
    def preprocess_data(self):
        for scan_type in self.analyzed_FRVM:
            for metric in self.analyzed_FRVM[scan_type]:
                if self.analyzed_FRVM[scan_type][metric] is not None:
                    self.analyzed_FRVM[scan_type][metric] = round(self.analyzed_FRVM[scan_type][metric], 4)
        for scan_type in self.analyzed_tSDN:
            for metric in self.analyzed_tSDN[scan_type]:
                if self.analyzed_tSDN[scan_type][metric] is not None:
                    self.analyzed_tSDN[scan_type][metric] = round(self.analyzed_tSDN[scan_type][metric], 4)

    def read_json(self, filename):
        with open(filename, "r") as f:
            return json.loads(f.read())

    def get_y_axis_of_metric(self, metric):
        yaxis_sS_Port1_9000_FRVM = []
        yaxis_sS_Port1_9000_tSDN = []
        for key in self.keys_sS_Port1_9000:
            y_FRVM = self.analyzed_FRVM.get(key).get(metric)
            y_tSDN = self.analyzed_tSDN.get(key).get(metric)
            yaxis_sS_Port1_9000_FRVM.append(y_FRVM)
            yaxis_sS_Port1_9000_tSDN.append(y_tSDN)
        
        yaxis_sT_Port1_9000_FRVM = []
        yaxis_sT_Port1_9000_tSDN = []
        for key in self.keys_sT_Port1_9000:
            y_FRVM = self.analyzed_FRVM.get(key).get(metric)
            y_tSDN = self.analyzed_tSDN.get(key).get(metric)
            yaxis_sT_Port1_9000_FRVM.append(y_FRVM)
            yaxis_sT_Port1_9000_tSDN.append(y_tSDN)
        
        yaxis_sU_Port1_9000_FRVM = []
        yaxis_sU_Port1_9000_tSDN = []
        for key in self.keys_sU_Port1_9000:
            y_FRVM = self.analyzed_FRVM.get(key).get(metric)
            y_tSDN = self.analyzed_tSDN.get(key).get(metric)
            yaxis_sU_Port1_9000_FRVM.append(y_FRVM)
            yaxis_sU_Port1_9000_tSDN.append(y_tSDN)
        
        yaxis_sS_Portdiscovered_FRVM = []
        yaxis_sS_Portdiscovered_tSDN = []
        for key in self.keys_sS_Portdiscovered:
            y_FRVM = self.analyzed_FRVM.get(key).get(metric)
            y_tSDN = self.analyzed_tSDN.get(key).get(metric)
            yaxis_sS_Portdiscovered_FRVM.append(y_FRVM)
            yaxis_sS_Portdiscovered_tSDN.append(y_tSDN)
        
        return yaxis_sS_Port1_9000_FRVM, yaxis_sS_Port1_9000_tSDN,\
            yaxis_sT_Port1_9000_FRVM, yaxis_sT_Port1_9000_tSDN,\
            yaxis_sU_Port1_9000_FRVM, yaxis_sU_Port1_9000_tSDN,\
            yaxis_sS_Portdiscovered_FRVM, yaxis_sS_Portdiscovered_tSDN

    def get_x_axis(self, y_axis_data):
        x_axis = []
        for i in range(0, 5):
            if y_axis_data[i] is not None:
                x_axis.append((i+1)*100)
        return x_axis
    
    def modify_y_axis(self, y_axis_data):
        new_y = []
        for data in y_axis_data:
            if data is not None:
                new_y.append(data)
        return new_y

    def draw_figures_of_metric(self, metric, index):
        yaxis_sS_Port1_9000_FRVM, yaxis_sS_Port1_9000_tSDN,\
            yaxis_sT_Port1_9000_FRVM, yaxis_sT_Port1_9000_tSDN,\
            yaxis_sU_Port1_9000_FRVM, yaxis_sU_Port1_9000_tSDN,\
            yaxis_sS_Portdiscovered_FRVM, yaxis_sS_Portdiscovered_tSDN = self.get_y_axis_of_metric(metric)
        
        figure_sS_Port1_9000 = plt.figure(index+1)
        tmp = self.get_x_axis(yaxis_sS_Port1_9000_FRVM)
        tmp2 = self.modify_y_axis(yaxis_sS_Port1_9000_FRVM)
        plt.plot(self.get_x_axis(yaxis_sS_Port1_9000_FRVM), self.modify_y_axis(yaxis_sS_Port1_9000_FRVM), linestyle='-', marker='o', label='FRVM')
        plt.plot(self.get_x_axis(yaxis_sS_Port1_9000_tSDN), self.modify_y_axis(yaxis_sS_Port1_9000_tSDN), linestyle='-', marker='o', label='tSDN')
        plt.ylabel(self.y_label[metric])
        plt.xlabel(self.x_label)
        plt.legend()
        for xy in zip(self.get_x_axis(yaxis_sS_Port1_9000_FRVM), self.modify_y_axis(yaxis_sS_Port1_9000_FRVM)):                                       # <--
            plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
        for xy in zip(self.get_x_axis(yaxis_sS_Port1_9000_tSDN), self.modify_y_axis(yaxis_sS_Port1_9000_tSDN)):                                       # <--
            plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
        plt.savefig("./figures/{}_sS_Port1_9000.png".format(metric))

        figure_sT_Port1_9000 = plt.figure(index+2)
        plt.plot(self.get_x_axis(yaxis_sT_Port1_9000_FRVM), self.modify_y_axis(yaxis_sT_Port1_9000_FRVM), linestyle='-', marker='o', label='FRVM')
        plt.plot(self.get_x_axis(yaxis_sT_Port1_9000_tSDN), self.modify_y_axis(yaxis_sT_Port1_9000_tSDN), linestyle='-', marker='o', label='tSDN')
        plt.ylabel(self.y_label[metric])
        plt.xlabel(self.x_label)
        plt.legend()
        for xy in zip(self.get_x_axis(yaxis_sT_Port1_9000_FRVM), self.modify_y_axis(yaxis_sT_Port1_9000_FRVM)):                                       # <--
            plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
        for xy in zip(self.get_x_axis(yaxis_sT_Port1_9000_tSDN), self.modify_y_axis(yaxis_sT_Port1_9000_tSDN)):                                       # <--
            plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
        plt.savefig("./figures/{}_sT_Port1_9000.png".format(metric))

        if self.check_data_valid(yaxis_sU_Port1_9000_FRVM):
            figure_sU_Port1_9000 = plt.figure(index+3)
            plt.plot(self.x_axis, yaxis_sU_Port1_9000_FRVM, linestyle='-', marker='o', label='FRVM')
            plt.plot(self.x_axis, yaxis_sU_Port1_9000_tSDN, linestyle='-', marker='o', label='tSDN')
            plt.ylabel(self.y_label[metric])
            plt.xlabel(self.x_label)
            plt.legend()
            for xy in zip(self.x_axis, yaxis_sU_Port1_9000_FRVM):                                       # <--
                plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            for xy in zip(self.x_axis, yaxis_sU_Port1_9000_tSDN):                                       # <--
                plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            # plt.show()
            plt.savefig("./figures/{}_sU_Port1_9000.png".format(metric))

        if self.check_data_valid(yaxis_sS_Portdiscovered_FRVM):
            figure_sS_Portdiscovered_FRVM = plt.figure(index+4)
            plt.plot(self.x_axis, yaxis_sS_Portdiscovered_FRVM, linestyle='-', marker='o', label='FRVM')
            plt.plot(self.x_axis, yaxis_sS_Portdiscovered_tSDN, linestyle='-', marker='o', label='tSDN')
            plt.ylabel(self.y_label[metric])
            plt.xlabel(self.x_label)
            plt.legend()
            for xy in zip(self.x_axis, yaxis_sS_Portdiscovered_FRVM):                                       # <--
                plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            for xy in zip(self.x_axis, yaxis_sS_Portdiscovered_tSDN):                                       # <--
                plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
            plt.savefig("./figures/{}_sS_Portdiscovered.png".format(metric))

    def check_data_valid(self, data_list):
        for data in data_list:
            if data:
                return True
        return False

    def run(self):
        metric = "scanning_success_probability"
        self.draw_figures_of_metric(metric, 0)
        self.draw_figures_of_metric("scanning_mean_min_of_all", 4)
        self.draw_figures_of_metric("scanning_mean_min_each_port", 8)


if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.run()