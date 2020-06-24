import sys
from ui.ui import UI
from logic.logic import Logic 

ui = UI()
logic = Logic()
ui.set_logic(logic)
logic.set_ui(ui)
ui.start_exploration(sys.argv[1:])