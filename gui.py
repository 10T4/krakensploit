import dearpygui.dearpygui as dpg
from addons.guiRunner import GuiRunner, get_dpg_values


dpg.create_context()

runner = GuiRunner(dpg)

with dpg.window(tag="MAIN"):

    with dpg.collapsing_header(label="Runner"):
        with dpg.group(horizontal=True):
            dpg.add_text("Target:")
            dpg.add_input_text(width=200, source="ip_address")
            dpg.add_text("/")
            dpg.add_input_text(width=22, source="prefix", default_value="32")

        with dpg.tree_node(label="NMap"):
            with dpg.group(horizontal=True):
                dpg.add_checkbox(source="nmap_network_services_scan", default_value=True)
                dpg.add_text("Run NMAP Scan")

            with dpg.group(horizontal=True):
                dpg.add_checkbox(source="scan_vuln", default_value=True)
                dpg.add_text("Vulnerability Scan")


        dpg.add_button(label="Run", callback=lambda: [runner.run(get_dpg_values(dpg)), runner.display_results()])

    with dpg.collapsing_header(label="Logger"):
        dpg.add_text(source="logger", default_value="Logger: Nothing to log")

    with dpg.collapsing_header(label="Output"):
        with dpg.tree_node(label="NMap"):
            with dpg.tab_bar():
                with dpg.tab(label="Network & Services Scan"):
                    dpg.add_text("Network & Services Scan Results")
                with dpg.tab(label="OS Detection"):
                    dpg.add_text("OS Detection Results")
                with dpg.tab(label="Vulnerability Scan"):
                    dpg.add_text("Vulnerability Scan Results")

    with dpg.collapsing_header(label="Settings"):
        dpg.add_text("Settings")

dpg.create_viewport(title='Krak&Sploit', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("MAIN", True)
dpg.start_dearpygui()
dpg.destroy_context()