from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charms.reactive import when, when_all, when_not
from charms.reactive import scopes


class InfobloxProvides(Endpoint):
    scope = scopes.UNIT

    @when_all('endpoint.{endpoint_name}.changed',
              'endpoint.{endpoint_name}.joined')
    def data_changed(self):
        set_flag(self.expand_name('{endpoint_name}.available'))
        clear_flag(self.expand_name('{endpoint_name}.configured'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

    def configure_principal(self, configuration):
        """Send principle infoblox configuration"""

        for relation in self.relations:
            relation.to_publish.update(configuration)

    def principal_charm_state(self):
        """Retrieve principal charm state
        :returns state: Principal neutron-api charm state
        :rtype state: Boolean"""

        return self.all_joined_units.received.get('neutron_api_ready')
