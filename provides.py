#!/usr/bin/python

import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class Infoblox(RelationBase):

    scope = scopes.GLOBAL

    @hook('{provides:infoblox-api}-relation-{joined, changed}')
    def peers_joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')


    @hook('{provides:infoblox-api}-relation-{broken, departed}')
    def peers_departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departing')
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def configure_plugin(self, dc_id=None, config=None):
        """Send principle infoblox connection information"""
        conversation = self.conversation()
        relation_info = {
            'dc_id': dc_id,
            'config': json.dumps(config),
        }
        conversation.set_remote(**relation_info)
