import dearpygui.dearpygui
from addons.scriptManager import scripts
from threading import Event
import threading
import time
import json

class GuiRunner:

    def __init__(self, dpg):
        self.scripts = []
        self.script_results = []
        self.dpg: dearpygui.dearpygui = dpg
        self.spinThread = None
        self.event = Event()
    
    def run(self, options):
        print("Running scripts")
        self.scripts = []
        self.script_results = []

        for option in options:
            if option.startswith("s_") and options[option]:
                self.scripts.append(option)

        self.event.clear()
        self.spinThread = threading.Thread(target=self.spin)
        self.spinThread.start()

        self.dpg.hide_item("download-button")

        for script in self.scripts:
            self.script_results.append({
                "script": script.replace("s_", ""),
                "result": self.run_script(script.replace("s_", ""), **options)
            })

            self.event.set()

        print("Scripts run")

    def spin(self):
        spinner_symbols = ["|", "/", "-", "\\"]
        while not self.event.is_set():
            for i in spinner_symbols:
                self.dpg.set_value("spinner", "Running" + " " + i)
                time.sleep(0.15)
        self.dpg.set_value("spinner", "")

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

        #return {'nmap': {'command_line': 'nmap -oX - -p- -Pn -sV -O --script=vuln 192.168.110.1/32', 'scaninfo': {'tcp': {'method': 'syn', 'services': '1-65535'}}, 'scanstats': {'timestr': 'Tue Apr 23 11:19:25 2024', 'elapsed': '229.90', 'uphosts': '1', 'downhosts': '0', 'totalhosts': '1'}}, 'scan': {'192.168.110.1': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.110.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'user-set'}, 'uptime': {'seconds': '584333', 'lastboot': 'Tue Apr 16 17:00:32 2024'}, 'tcp': {135: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 137: {'state': 'filtered', 'reason': 'no-response', 'name': 'netbios-ns', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 139: {'state': 'open', 'reason': 'syn-ack', 'name': 'netbios-ssn', 'product': 'Microsoft Windows netbios-ssn', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 445: {'state': 'open', 'reason': 'syn-ack', 'name': 'microsoft-ds', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 903: {'state': 'open', 'reason': 'syn-ack', 'name': 'vmware-auth', 'product': 'VMware Authentication Daemon', 'version': '1.10', 'extrainfo': 'Uses VNC, SOAP', 'conf': '10', 'cpe': '', 'script': {'ssl-ccs-injection': 'No reply from server (TIMEOUT)'}}, 913: {'state': 'open', 'reason': 'syn-ack', 'name': 'vmware-auth', 'product': 'VMware Authentication Daemon', 'version': '1.0', 'extrainfo': 'Uses VNC, SOAP', 'conf': '10', 'cpe': ''}, 3306: {'state': 'open', 'reason': 'syn-ack', 'name': 'mysql', 'product': 'MySQL', 'version': '8.2.0', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/a:mysql:mysql:8.2.0', 'script': {'mysql-vuln-cve2012-2122': 'ERROR: Script execution failed (use -d to debug)', 'vulners': '\n  cpe:/a:mysql:mysql:8.2.0: \n    \tPRION:CVE-2024-20969\t4.7\thttps://vulners.com/prion/PRION:CVE-2024-20969\n    \tPRION:CVE-2024-20967\t4.7\thttps://vulners.com/prion/PRION:CVE-2024-20967\n    \tPRION:CVE-2024-20985\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20985\n    \tPRION:CVE-2024-20977\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20977\n    \tPRION:CVE-2024-20975\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20975\n    \tPRION:CVE-2024-20973\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20973\n    \tPRION:CVE-2024-20963\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20963\n    \tPRION:CVE-2024-20961\t4.0\thttps://vulners.com/prion/PRION:CVE-2024-20961\n    \tPRION:CVE-2024-20981\t3.3\thttps://vulners.com/prion/PRION:CVE-2024-20981\n    \tPRION:CVE-2024-20971\t3.3\thttps://vulners.com/prion/PRION:CVE-2024-20971\n    \tPRION:CVE-2024-20965\t3.3\thttps://vulners.com/prion/PRION:CVE-2024-20965'}}, 5040: {'state': 'open', 'reason': 'syn-ack', 'name': '', 'product': '', 'version': '', 'extrainfo': '', 'conf': '', 'cpe': ''}, 5432: {'state': 'open', 'reason': 'syn-ack', 'name': 'postgresql', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}, 15100: {'state': 'open', 'reason': 'syn-ack', 'name': 'unknown', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': '', 'script': {'fingerprint-strings': '\n  DNSStatusRequestTCP: \n    mQ"t\n  GenericLines, NULL: \n    U.k(-R\n    1dE,\n  HTTPOptions: \n    XZnl\n    QWm)\n    yJ?~\n  RTSPRequest: \n    %:#t'}}, 15101: {'state': 'open', 'reason': 'syn-ack', 'name': 'unknown', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': '', 'script': {'fingerprint-strings': "\n  GenericLines, NULL: \n    nb-z\n    '{V@i\n    \\x9d`\n    /sCN\n    54(v\n    =onD\n    -#'B\n    \\xcbP\n    E-2Y\n    \\x88\n    QlCn\n    KCDa\n    -q7>"}}, 28252: {'state': 'open', 'reason': 'syn-ack', 'name': '', 'product': '', 'version': '', 'extrainfo': '', 'conf': '', 'cpe': ''}, 33060: {'state': 'open', 'reason': 'syn-ack', 'name': 'mysqlx', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': '', 'script': {'fingerprint-strings': '\n  DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: \n    Invalid message"\n    HY000\n  LDAPBindReq: \n    *Parse error unserializing protobuf message"\n    HY000\n  oracle-tns: \n    Invalid message-frame."\n    HY000'}}, 45769: {'state': 'open', 'reason': 'syn-ack', 'name': '', 'product': '', 'version': '', 'extrainfo': '', 'conf': '', 'cpe': ''}, 49664: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 49665: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 49666: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 49667: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 49668: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}, 49669: {'state': 'open', 'reason': 'syn-ack', 'name': 'msrpc', 'product': 'Microsoft Windows RPC', 'version': '', 'extrainfo': '', 'conf': '10', 'cpe': 'cpe:/o:microsoft:windows'}}, 'hostscript': [{'id': 'smb-vuln-ms10-054', 'output': 'false'}, {'id': 'smb-vuln-ms10-061', 'output': 'Could not negotiate a connection:SMB: Failed to receive bytes: ERROR'}, {'id': 'samba-vuln-cve-2012-1182', 'output': 'Could not negotiate a connection:SMB: Failed to receive bytes: ERROR'}], 'portused': [{'state': 'open', 'proto': 'tcp', 'portid': '135'}, {'state': 'closed', 'proto': 'tcp', 'portid': '1'}, {'state': 'closed', 'proto': 'udp', 'portid': '41050'}], 'osmatch': [{'name': 'Microsoft Windows 10 1607', 'accuracy': '100', 'line': '69748', 'osclass': [{'type': 'general purpose', 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '10', 'accuracy': '100', 'cpe': ['cpe:/o:microsoft:windows_10:1607']}]}]}}}
        return script.run_script(**scriptArgs)
        
    def display_results(self):
        print("Displaying results")
        print(self.script_results)
        logs = ""
        if self.dpg.get_value("logger") != "Logger: Nothing to log":
            logs = self.dpg.get_value("logger") + "\n\n"

        self.dpg.delete_item("tabs", children_only=True)

        for script_result in self.script_results:
            logs += "---------------------------------------------\n"
            logs += str(script_result["script"]) + "\n"
            logs += str(script_result["result"]) + "\n\n"

            self.dpg.add_tab(tag=script_result["script"] + "_tab", label=script_result["script"], parent="tabs")

            self.dpg.add_table(tag=script_result["script"]+"_table", header_row=True, sortable=True, reorderable=True, context_menu_in_body=True, parent=script_result["script"] + "_tab")
            
            formatted = scripts[script_result["script"]].format_to_table(script_result["result"])
            
            for item in formatted["headers"]:
                self.dpg.add_table_column(parent=script_result["script"] + "_table", label=item)
            for item in formatted["rows"]:
                with self.dpg.table_row(parent=script_result["script"] + "_table"):
                    for i in item:
                        self.dpg.add_text(i, wrap=(600 / (formatted["headers"].__len__()-1)))
            
        self.dpg.set_value("logger", logs)
        self.dpg.show_item("download-button")
    
    def save_results(self):
        print("Saving results")
        with open("results.json", "w") as f:
            json.dump(self.script_results, f, indent=4)

        print("Results saved")

    def setup_inputs(self):
        self.dpg.add_string_value(default_value="", tag="spinner")
        self.dpg.add_string_value(default_value="Logger: Nothing to log", tag="logger")

        self.dpg.delete_item("inputs", children_only=True)
        for script in scripts:
            self.dpg.add_tab(label=script, parent="inputs", tag=script + "_inputs")

            with self.dpg.group(horizontal=True, parent=script + "_inputs"):
                with self.dpg.value_registry():
                    self.dpg.add_bool_value(default_value=True, tag=("s_" + script))
                self.dpg.add_checkbox(source=("s_" + script))
                self.dpg.add_text("Enable " + script)

            for input in scripts[script].gui_inputs():
                input_group_tag = script + "_" + input["id"] + "_group"
                input_tag = script + "_" + input["id"]
                self.dpg.add_group(parent=script + "_inputs", tag=input_group_tag, horizontal=True)
                if input["type"] == "text":
                    self.dpg.add_string_value(default_value="", tag=input_tag)
                    self.dpg.add_input_text(width=200, source=input_tag, parent=input_group_tag)
                elif input["type"] == "number":
                    self.dpg.add_int_value(default_value=32, tag=input_tag)
                    self.dpg.add_input_int(width=200, source=input_tag, parent=input_group_tag)
                elif input["type"] == "checkbox":
                    self.dpg.add_bool_value(default_value=False, tag=input_tag)
                    self.dpg.add_checkbox(source=input_tag, parent=input_group_tag)
                elif input["type"] == "file":
                    self.dpg.add_string_value(default_value="", tag=input_tag)
                    self.dpg.add_button(label="Choose file", callback=lambda s: [self.request_file(s.replace('_button', ''))], parent=input_group_tag, tag=input_tag + "_button")
                    self.dpg.add_text(source=input_tag, parent=input_group_tag)
                elif input["type"] == "output":
                    self.dpg.add_bool_value(default_value=False, tag=input_tag)
                    self.dpg.add_checkbox(source=input_tag, parent=input_group_tag)

                self.dpg.add_text(input["label"], parent=input_group_tag)


    def get_dpg_values(self):
        values = {}

        for script in scripts:
            values["s_" + script] = self.dpg.get_value("s_" + script)

            for input in scripts[script].gui_inputs():
                if input["type"] == "text":
                    values[script + "_" + input["id"]] = self.dpg.get_value(script + "_" + input["id"])
                elif input["type"] == "number":
                    values[script + "_" + input["id"]] = self.dpg.get_value(script + "_" + input["id"])
                elif input["type"] == "checkbox":
                    values[script + "_" + input["id"]] = self.dpg.get_value(script + "_" + input["id"])
                elif input["type"] == "file":
                    values[script + "_" + input["id"]] = self.dpg.get_value(script + "_" + input["id"])

        print(values)

        return values
    
    def request_file(self, for_tag):
        print(self.dpg.get_value(for_tag))

        def callback(s, a):
            print(a['file_path_name'])
            self.dpg.set_value(for_tag, a['file_path_name'])

        with self.dpg.file_dialog(callback=callback, width=400, height=400, show=True, directory_selector=False, file_count=1, modal=True, label="Choose file"):
            self.dpg.add_file_extension(".txt")
