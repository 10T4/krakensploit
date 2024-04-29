import dearpygui.dearpygui as dpg
from addons.guiRunner import GuiRunner

runner = GuiRunner(dpg)

dpg.create_context()

with dpg.window(tag="MAIN"):

    with dpg.collapsing_header(label="Runner"):
        dpg.add_tab_bar(tag="inputs")
        with dpg.value_registry():
            runner.setup_inputs()

        with dpg.group(horizontal=True):
            dpg.add_button(label="Run", callback=lambda: [runner.run(runner.get_dpg_values()), runner.display_results()])
            dpg.add_text(source="spinner", default_value="")
            dpg.add_button(tag="download-button", label="Download JSON", callback=lambda: runner.save_results(), show=False)

    with dpg.collapsing_header(label="Logger"):
        dpg.add_text(source="logger", default_value="Logger: Nothing to log", wrap=600)

    with dpg.collapsing_header(label="Output"):
        dpg.add_tab_bar(tag="tabs")

    with dpg.collapsing_header(label="Settings"):
        dpg.add_text("Settings")

dpg.create_viewport(title='Krak&Sploit', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("MAIN", True)
dpg.start_dearpygui()
dpg.destroy_context()