#!/usr/bin/python
#
# Copyright (c) 2011 Red Hat, Inc.
#
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import base

from mock import patch

from gofer.messaging import Envelope

from pulp.devel import mock_agent
from pulp.server.agent.direct.pulpagent import PulpAgent as DirectAgent
from pulp.server.agent.direct.services import HeartbeatListener


REPO_ID = 'repo_1'
DETAILS = {}
BINDINGS = [
    {'type_id':'yum',
     'repo_id':REPO_ID,
     'details':DETAILS,}
]
CONSUMER = {
    'id':'gc',
    'certificate':'XXX',
}
UNIT = {
    'type_id':'rpm',
    'unit_key':{
        'name':'zsh',
    }
}
UNITS = [UNIT,]
OPTIONS = {
    'xxx':True,
}

TASKID = 'TASK-123'


class TestAgent(base.PulpServerTests):
    
    def setUp(self):
        base.PulpServerTests.setUp(self)
        mock_agent.install()
        mock_agent.reset()
    
    def test_unregistered(self):
        # Test
        agent = DirectAgent(CONSUMER)
        agent.consumer.unregistered()
        # Verify
        mock_agent.Consumer.unregistered.assert_called_once_with()
        
    def test_bind(self):
        # Test
        agent = DirectAgent(CONSUMER)
        result = agent.consumer.bind(BINDINGS, OPTIONS)
        # Verify
        mock_agent.Consumer.bind.assert_called_once_with(BINDINGS, OPTIONS)
        
    def test_unbind(self):
        # Test
        agent = DirectAgent(CONSUMER)
        result = agent.consumer.unbind(BINDINGS, OPTIONS)
        # Verify
        mock_agent.Consumer.unbind.assert_called_once_with(BINDINGS, OPTIONS)
        
    def test_install_content(self):
        # Test
        agent = DirectAgent(CONSUMER)
        result = agent.content.install(UNITS, OPTIONS)
        # Verify
        mock_agent.Content.install.assert_called_once_with(UNITS, OPTIONS)
        
    def test_update_content(self):
        # Test
        agent = DirectAgent(CONSUMER)
        result = agent.content.update(UNITS, OPTIONS)
        # Verify
        mock_agent.Content.update.assert_called_once_with(UNITS, OPTIONS)
        
    def test_uninstall_content(self):
        # Test
        agent = DirectAgent(CONSUMER)
        result = agent.content.uninstall(UNITS, OPTIONS)
        # Verify
        mock_agent.Content.uninstall.assert_called_once_with(UNITS, OPTIONS)

    def test_profile_send(self):
        # Test
        agent = DirectAgent(CONSUMER)
        print agent.profile.send()
        # Verify
        mock_agent.Profile.send.assert_called_once_with()

    def test_status(self):
        # Setup
        listener = HeartbeatListener('queue')
        envelope = Envelope(heartbeat=dict(uuid='A', next=10))
        listener.dispatch(envelope)
        # Test
        result = DirectAgent.status(['A','B'])
        # Verify
        self.assertEqual(len(result), 2)
        # A
        alive, next_heartbeat, details = result['A']
        self.assertTrue(alive)
        self.assertTrue(isinstance(next_heartbeat, basestring))
        self.assertTrue(isinstance(details, dict))
        # B
        alive, last_heartbeat, details = result['B']
        self.assertFalse(alive)
        self.assertTrue(last_heartbeat is None)
        self.assertTrue(isinstance(details, dict))

    def test_cancel(self):
        # Test
        task_id = '123'
        agent = DirectAgent(CONSUMER)
        agent.cancel(task_id)
        # Verify
        criteria = {'eq': task_id}
        mock_agent.Admin.cancel.assert_called_once_with(criteria=criteria)
