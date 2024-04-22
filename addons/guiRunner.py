from addons.scriptManager import scripts

class GuiRunner:

    def __init__(self, dpg):
        self.scripts = []
        self.script_results = []
        set_dpg_values(dpg)
        self.dpg = dpg
    
    def run(self, scripts):
        print("Running scripts")
        self.scripts = [k for k in scripts if 's_' in k]
        self.script_results = []

        for script in self.scripts:
            self.script_results.append(self.run_script(script.replace("s_", ""), **scripts))

        print("Scripts run")

    def run_script(self, scriptName, **args):
        print("Running script " + scriptName)
        
        if not scriptName in scripts:
            print("Invalid script")
            return
        
        script = scripts[scriptName]

        scriptArgs = {}

        for arg in args:
            if arg.startswith(scriptName):
                scriptArgs[arg.replace(scriptName + "_", "")] = args[arg]


        return script.run_script(**scriptArgs)
        
    def display_results(self):
        print("Displaying results")
        print(self.script_results)
        logs = ""
        if self.dpg.get_value("logger") != "Logger: Nothing to log":
            logs = self.dpg.get_value("logger") + "\n\n"

        for script_result in self.script_results:
            logs += self.scripts[self.script_results.index(script_result)] + "\n"
            logs += str(script_result) + "\n\n"

        self.dpg.set_value("logger", logs)

def set_dpg_values(dpg):
    with dpg.value_registry():
        dpg.add_bool_value(default_value=True, tag="nmap_network_services_scan")
        dpg.add_string_value(default_value="Logger: Nothing to log", tag="logger")

        # NMAP
        dpg.add_string_value(default_value="", tag="ip_address")
        dpg.add_string_value(default_value="32", tag="prefix")
        dpg.add_bool_value(default_value=True, tag="scan_vuln")

def get_dpg_values(dpg):
    return {
        "s_nmap": dpg.get_value("nmap_network_services_scan"),
        "logger": dpg.get_value("logger"),
        "nmap_ip_address": dpg.get_value("ip_address"),
        "nmap_prefix": dpg.get_value("prefix"),
        "nmap_scan_vuln": dpg.get_value("scan_vuln")
    }