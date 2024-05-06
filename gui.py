import dearpygui.dearpygui as dpg
from addons.guiRunner import GuiRunner

runner = GuiRunner(dpg)

dpg.create_context()

width, height, channels, data = dpg.load_image("addons/krak&logo.png")

with dpg.texture_registry(show=False):
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="logo")

with dpg.window(tag="MAIN"):

    with dpg.collapsing_header(label="Runner", default_open=True):
        dpg.add_tab_bar(tag="inputs")
        with dpg.value_registry():
            runner.setup_inputs()

        with dpg.group(horizontal=True):
            dpg.add_button(label="Run", callback=lambda: [runner.run(runner.get_dpg_values()), runner.display_results()])
            dpg.add_text(source="spinner", default_value="")
            dpg.add_button(tag="download-button", label="Download JSON", callback=lambda: runner.save_results(), show=False)

    with dpg.collapsing_header(label="Logger"):
        dpg.add_text(source="logger", default_value="Logger: Nothing to log", wrap=600)

    with dpg.collapsing_header(label="Output", default_open=True):
        dpg.add_tab_bar(tag="tabs")

    with dpg.collapsing_header(label="Settings"):
        dpg.add_text("Settings")

with dpg.window(tag="welcome", label="Welcome", width=300, height=300, no_collapse=True, no_move=True, no_resize=True, no_scrollbar=True, no_saved_settings=True, show=True):
    dpg.add_text("Krak&Sploit", pos=(112, 20), wrap=300)
    dpg.add_image("logo", width=200, height=200, pos=(50, 50))
    dpg.add_text("   A simple tool to scan for vulnerabilities in your network", wrap=280, pos=(40, 250))

dpg.create_viewport(title='Krak&Sploit', width=600, height=600, small_icon="addons/krak&logo.ico", large_icon="addons/krak&logo.ico")
dpg.setup_dearpygui()
dpg.set_viewport_resize_callback(lambda: [dpg.configure_item("welcome", pos=(dpg.get_viewport_client_width() // 2 - 150, dpg.get_viewport_client_height() // 2 - 150)), dpg.configure_item("error", pos=(dpg.get_viewport_client_width() // 2 - 150, dpg.get_viewport_client_height() // 2 - 150)) if dpg.does_item_exist("error") else None])
dpg.show_viewport()
dpg.set_primary_window("MAIN", True)
dpg.start_dearpygui()
dpg.destroy_context()