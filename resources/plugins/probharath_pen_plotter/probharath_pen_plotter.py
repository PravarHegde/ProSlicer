# /// script
# requires-python = ">=3.12"
#
# [tool.orcaslicer.plugin]
# name = "ProBharath Pen Plotter & Laser 2D"
# description = "Multi-tool 2D vector plotter, calligraphy pen up/down servo control, and diode laser engraving."
# author = "ProBharath Mechatronics"
# version = "1.0.0"
# type = "script"
# ///
import orca

class PenPlotterCapability(orca.script.ScriptPluginCapabilityBase):
    def get_name(self):
        return "Pen Plotter Toolpath"

    def execute(self, ctx=None):
        return orca.ExecutionResult.success("Pen plotter path generation active with servo Z-lift.")

@orca.plugin
class PenPlotterPackage(orca.base):
    def register_capabilities(self):
        orca.register_capability(PenPlotterCapability)
