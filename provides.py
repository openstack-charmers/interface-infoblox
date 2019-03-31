from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charms.reactive import when, when_all, when_not
from charms.reactive import scopes


class InfobloxProvides(Endpoint):
    scope = scopes.GLOBAL


    @when_all('endpoint.{endpoint_name}.changed',
              'endpoint.{endpoint_name}.joined')
    @when_not('endpoint.{endpoint_name}.changed.neutron_api_ready')
    def joined(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.connected'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.configured'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.connected'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.departed'))

    @when('endpoint.{endpoint_name}.changed.neutron_api_ready')
    def neutron_ready(self):
        clear_flag(
            self.expand_name(
                'endpoint.{endpoint_name}.changed.neutron_api_ready'))
        set_flag(self.expand_name('endpoint.{endpoint_name}.neutron_server_ready'))

    def configure_principal(self, configuration):
        """Send principle infoblox configuration"""

        for relation in self.relations:
            relation.to_publish.update(configuration)
