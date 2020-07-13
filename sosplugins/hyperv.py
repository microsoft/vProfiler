from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Hyperv(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):
    """Hyper-V client information"""

    plugin_name="hyperv"

    def setup(self):

        self.add_copy_spec([
            "/sys/bus/vmbus/drivers/",
            "/sys/bus/vmbus/devices/*/*",
            "/boot/config-*"
        ])

        self.add_cmd_output("lsvmbus -vv")
        self.add_cmd_output("lspci -vv")

