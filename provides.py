#!/usr/bin/python

import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class Infoblox(RelationBase):

    scope = scopes.GLOBAL

    @hook('{provides:infoblox}-relation-joined')
    def infoblox_joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')

    @hook('{provides:infoblox}-relation-changed')
    def infoblox_changed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.configured')
        if conv.get_remote('configured'):
            conv.set_state('{relation_name}.configured')
        if conv.get_remote('create-defs'):
            conv.set_state('infoblox.create-defs')

    @hook('{provides:infoblox}-relation-{broken, departed}')
    def infoblox_departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departing')
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def configure_principal(self, config, dc_id=None):
        """Send principle infoblox connection information"""
        conv = self.conversation()
        relation_info = {
            'dc_id': dc_id,
            'config': json.dumps(config),
        }
        conv.set_remote(**relation_info)

    def migrate_principal(self, dc_id=None, config=None):
        """Request a restart of principle services"""
        conv = self.conversation()
        relation_info = {
            'migrate': True
        }
        conv.set_remote(**relation_info)
