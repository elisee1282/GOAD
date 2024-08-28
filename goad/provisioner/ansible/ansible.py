import ansible_runner
import time
import yaml
from goad.utils import *
from goad.log import Log
from goad.provisioner.provisioner import Provisioner


class Ansible(Provisioner):

    @staticmethod
    def get_inventory(lab_name, provider_name):
        inventory = []
        Log.info('Loading inventory')
        # Lab inventory
        lab_inventory = get_lab_inventory_path(lab_name)
        if os.path.isfile(lab_inventory):
            inventory.append(lab_inventory)
            Log.success(f'Lab inventory : {lab_inventory} file found')
        # Provider inventory
        provider_inventory = get_provider_inventory_path(lab_name, provider_name)
        if os.path.isfile(provider_inventory):
            inventory.append(provider_inventory)
            Log.success(f'Provider inventory : {provider_inventory} file found')
        # Global inventory
        global_inventory = get_global_inventory_path()
        if os.path.isfile(global_inventory):
            inventory.append(global_inventory)
            Log.success(f'Global inventory : {global_inventory} file found')
        return inventory

    @staticmethod
    def get_playbook_list(lab_name):
        Log.info('Loading playbook list')
        playbook_organisation_file = get_playbooks_lab_config()
        playbook_list = []
        with open(playbook_organisation_file, 'r') as playbooks:
            data_loaded = yaml.safe_load(playbooks)
        if lab_name in data_loaded:
            playbook_datas = data_loaded[lab_name]
        else:
            playbook_datas = data_loaded['default']

        # validate playbooks
        for playbook in playbook_datas:
            playbook_path = get_provisioner_path() + os.path.sep + playbook
            if not os.path.isfile(playbook_path):
                Log.error(f'{playbook} not valid, file {playbook_path} not found')
            else:
                playbook_list.append(playbook)
                Log.success(f'{playbook} file found')
        return playbook_list

    def run(self, playbook=None):
        inventory = self.get_inventory(self.lab_name, self.provider_name)
        provision_result = False
        if playbook is None:
            playbooks = self.get_playbook_list(self.lab_name)
            for playbook in playbooks:
                provision_result = self.run_playbook(playbook, inventory)
                if not provision_result:
                    Log.error(f'Something wrong during the provisioning task : {playbook}')
                    return False
        else:
            provision_result = self.run_playbook(playbook, inventory)
        return provision_result

    def run_from(self, task):
        inventory = self.get_inventory(self.lab_name, self.provider_name)
        playbooks = self.get_playbook_list(self.lab_name)

        if task == '' or task is None:
            Log.error('Missing playbook to start from')
            Log.info('Playbook list :')
            for playbook in playbooks:
                Log.info(f' - {playbook}')
            return False

        skip = True
        for playbook in playbooks:
            if playbook == task:
                skip = False
            if skip:
                Log.info(f'skip {playbook}')
            else:
                provision_result = self.run_playbook(playbook, inventory)
                if not provision_result:
                    Log.error(f'Something wrong during the provisioning task : {playbook}')
                    return False
        return True

    def run_playbook(self, playbook, inventories, tries=3, timeout=30):
        # abstract
        pass



