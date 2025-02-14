# Copyright 2019 Open Source Robotics Foundation, Inc.
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

"""Module for the Shutdown action."""

import logging
from typing import List
from typing import Text
from typing import Tuple
from typing import Type

from launch.frontend import Entity
from launch.frontend import expose_action
from launch.frontend import Parser
from typing_extensions import Self

from .emit_event import EmitEvent
from ..action import ActionParsedDict
from ..events import Shutdown as ShutdownEvent
from ..events.process import ProcessExited
from ..launch_context import LaunchContext
from ..substitution import Substitution


_logger = logging.getLogger(name='launch')


class ShutdownParsedDict(ActionParsedDict, total=False):
    reason: List[Substitution]


@expose_action('shutdown')
class Shutdown(EmitEvent):
    """Action that shuts down a launched system by emitting Shutdown when executed."""

    def __init__(self, *, reason: Text = 'reason not given', **kwargs):
        super().__init__(event=ShutdownEvent(reason=reason), **kwargs)

    @classmethod
    def parse(cls, entity: Entity, parser: Parser
              ) -> Tuple[Type[Self], ShutdownParsedDict]:
        """Return `Shutdown` action and kwargs for constructing it."""
        _, kwargs = super().parse(entity, parser)
        reason = entity.get_attr('reason', optional=True)
        new_kwargs = ShutdownParsedDict(**kwargs)
        if reason:
            new_kwargs['reason'] = parser.parse_substitution(reason)
        return cls, new_kwargs

    def execute(self, context: LaunchContext) -> None:
        """Execute the action."""
        try:
            event = context.locals.event
        except AttributeError:
            event = None

        if isinstance(event, ProcessExited):
            _logger.info('process[{}] was required: shutting down launched system'.format(
                event.process_name))

        super().execute(context)
