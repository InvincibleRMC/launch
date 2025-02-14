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

"""Module for the SetEnvironmentVariable action."""

from typing import Any
from typing import List
from typing import Tuple
from typing import Type

from typing_extensions import Self

from ..action import Action
from ..action import ActionParsedDict
from ..frontend import Entity
from ..frontend import expose_action
from ..frontend import Parser
from ..launch_context import LaunchContext
from ..some_substitutions_type import SomeSubstitutionsType
from ..substitution import Substitution
from ..utilities import normalize_to_list_of_substitutions
from ..utilities import perform_substitutions


class SetEnvironmentVariableParsedDict(ActionParsedDict):
    name: List[Substitution]
    value: List[Substitution]


@expose_action('set_env')
class SetEnvironmentVariable(Action):
    """Action that sets an environment variable."""

    def __init__(
        self,
        name: SomeSubstitutionsType,
        value: SomeSubstitutionsType,
        **kwargs: Any
    ) -> None:
        """Create a SetEnvironmentVariable action."""
        super().__init__(**kwargs)
        self.__name = normalize_to_list_of_substitutions(name)
        self.__value = normalize_to_list_of_substitutions(value)

    @classmethod
    def parse(
        cls,
        entity: Entity,
        parser: Parser,
    ) -> Tuple[Type[Self], SetEnvironmentVariableParsedDict]:
        """Parse a 'set_env' entity."""
        _, kwargs = super().parse(entity, parser)
        new_kwargs = SetEnvironmentVariableParsedDict(
            name=parser.parse_substitution(entity.get_attr('name')),
            value=parser.parse_substitution(entity.get_attr('value')),
            **kwargs
        )
        return cls, new_kwargs

    @property
    def name(self) -> List[Substitution]:
        """Getter for the name of the environment variable to be set."""
        return self.__name

    @property
    def value(self) -> List[Substitution]:
        """Getter for the value of the environment variable to be set."""
        return self.__value

    def execute(self, context: LaunchContext) -> None:
        """Execute the action."""
        context.environment[perform_substitutions(context, self.name)] = \
            perform_substitutions(context, self.value)
        return None
