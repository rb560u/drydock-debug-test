# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test Validation Rule Unique Network"""

import re

from drydock_provisioner.orchestrator.orchestrator import Orchestrator
from drydock_provisioner.orchestrator.validations.validator import Validator


class TestMtu(object):
    def test_mtu(self, mocker, deckhand_ingester, drydock_state, input_files):

        input_file = input_files.join("validation.yaml")
        design_ref = "file://%s" % str(input_file)

        orch = Orchestrator(state_manager=drydock_state, ingester=deckhand_ingester)

        status, site_design = Orchestrator.get_effective_site(orch, design_ref)

        message_list = Validator.mtu_rational(site_design)
        msg = message_list[0].to_dict()

        assert msg.get('message') == 'Mtu'
        assert msg.get('error') is False
        assert len(message_list) == 1

    def test_invalid_mtu(self, mocker, deckhand_ingester, drydock_state, input_files):

        input_file = input_files.join("invalid_validation.yaml")
        design_ref = "file://%s" % str(input_file)

        orch = Orchestrator(state_manager=drydock_state, ingester=deckhand_ingester)

        status, site_design = Orchestrator.get_effective_site(orch, design_ref)

        message_list = Validator.mtu_rational(site_design)

        regex = re.compile('Mtu Error: Mtu must be between 1400 and 64000; on Network .+')
        regex_1 = re.compile('Mtu Error: Mtu must be <= the parent Network Link; for Network .+')

        for msg in message_list:
            msg = msg.to_dict()
            assert msg.get('error')
            assert regex.match(msg.get('message')) is not None or regex_1.match(msg.get('message')) is not None

        assert len(message_list) == 4
