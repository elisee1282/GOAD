from goad.provider.vagrant.vagrant import VagrantProvider
from goad.utils import *


class VirtualboxProvider(VagrantProvider):
    provider_name = VIRTUALBOX
    default_provisioner = PROVISIONING_LOCAL
    allowed_provisioners = [PROVISIONING_LOCAL, PROVISIONING_RUNNER, PROVISIONING_DOCKER]

    def check(self):
        checks = [
            super().check(),
            self.command.check_virtualbox()
        ]
        return all(checks)
