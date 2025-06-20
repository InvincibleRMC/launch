# Copyright 2018 Open Source Robotics Foundation, Inc.
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

from typing import ItemsView
from typing import List
from typing import OrderedDict
from typing import Text


# This was copy/pasted from ros2launch.api to avoid a rclpy dependency in launch_testing
def parse_launch_arguments(launch_arguments: List[Text]) -> ItemsView[Text, Text]:
    """Parse the given launch arguments from the command line, into list of tuples for launch."""
    parsed_launch_arguments: OrderedDict[Text, Text] = OrderedDict()  # type: ignore
    for argument in launch_arguments:
        count = argument.count(':=')
        if count == 0 or argument.startswith(':=') or (count == 1 and argument.endswith(':=')):
            raise RuntimeError(
                "malformed launch argument '{}', expected format '<name>:=<value>'"
                .format(argument))
        name, value = argument.split(':=', maxsplit=1)
        parsed_launch_arguments[name] = value  # last one wins is intentional
    return parsed_launch_arguments.items()
