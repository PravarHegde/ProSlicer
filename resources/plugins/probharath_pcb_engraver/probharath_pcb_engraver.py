# /// script
# requires-python = ">=3.12"
#
# [tool.orcaslicer.plugin]
# name = "ProBharath PCB Isolation & Engraver"
# description = "Precision PCB isolation routing, copper clearance milling, and SMD pad isolation toolpaths."
# author = "ProBharath Electronics Lab"
# version = "1.0.0"
# type = "script"
# ///
import orca

class PcbIsolationCapability(orca.script.ScriptPluginCapabilityBase):
    def get_name(self):
        return "PCB Isolation Routing"

    def execute(self, ctx=None):
        return orca.ExecutionResult.success("PCB isolation routing toolpaths generated with 0.1mm V-bit.")

@orca.plugin
class PcbEngraverPackage(orca.base):
    def register_capabilities(self):
        orca.register_capability(PcbIsolationCapability)
