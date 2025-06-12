"""Implementation of must_include_collections rule."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ansiblelint.constants import FILENAME_KEY, LINE_NUMBER_KEY
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task, get_first_cmd_arg

import re

if TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable

C_MANDATORY_COLLECTIONS: str = "mandatorycollections"

ID: str = "must_include_collections"
DESC: str = """Rule to check if mandatory collections are included.

- Options

  - ``mandatorycollections`` lists the required collections

- Configuration

  .. code-block:: yaml
  
  rules:
    must_include_collections:
      mandatorycollections:
        - internal.collection.role
"""

MANDATORY_COLLECTIONS: typing.FrozenSet[str] = frozenset("""
internal.collection.role
""".split())

class MustIncludeCollectionsRule(AnsibleLintRule):
    """Playbooks must include mandatory collections"""

    id : str = ID
    shortdesc: str = "Must Include Collections"
    description: str = DESC
    severity = "VERY_HIGH"
    tags = ["email", "customer"]
    version_changed = "5.0.11"

    def mandatory_collections(self):
        mandatory = self.get_config(C_MANDATORY_COLLECTIONS)
        if mandatory:
            return frozenset(mandatory)
        
        return MANDATORY_COLLECTIONS
    
    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        if file.kind != "playbook":
            return []
        
        results = []
        for checkcollection in self.mandatory_collections():
            if checkcollection not in data["collections"]:
                results.append(
                    self.create_matcherror(
                        message=("Collection {0} needs to be included".format(checkcollection)),
                        filename=file
                    )
                )

        return results