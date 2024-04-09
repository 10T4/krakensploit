import dearpygui.dearpygui as dpg

def save_callback():
    print(dpg.get_value("string_value"))

dpg.create_context()

with dpg.value_registry():
    dpg.add_string_value(default_value="Default string", tag="string_value")

dpg.create_viewport()
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window", True)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string", source="string_value")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()