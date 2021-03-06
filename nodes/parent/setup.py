#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from setuptools import setup, find_packages

setup(
    name='pulp_node_parent',
    version='2.3.0',
    license='GPLv2+',
    packages=find_packages(),
    author='Pulp Team',
    author_email='pulp-list@redhat.com',
    entry_points={
        'pulp.distributors': [
            'distributor = pulp_node.distributors.http.distributor:entry_point',
        ],
        'pulp.profilers': [
            'profiler = pulp_node.profilers.nodes:entry_point'
        ]
    }
)
