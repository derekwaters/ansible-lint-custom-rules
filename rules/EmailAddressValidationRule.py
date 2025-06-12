"""Implementation of email-address-validation rule."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ansiblelint.constants import FILENAME_KEY, LINE_NUMBER_KEY
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task, get_first_cmd_arg

import re

if TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable

C_WHITELIST_EMAIL_DOMAINS: str = "whitelistemaildomains"

ID: str = "email_address_validation"
DESC: str = """Rule to check if any emails sent from modules are to defined domains.

- Options

  - ``whitelistemaildomains`` lists the allowed email domains

- Configuration

  .. code-block:: yaml
  
  rules:
    email_address_validation:
      whitelistemaildomains:
        - customer.com.au
        - customer.com
        - cust.com.au
"""

WHITELIST_EMAIL_DOMAINS: typing.FrozenSet[str] = frozenset("""
customer.com.au
customer.com
cust.com.au
""".split())

class EmailAddressValidationRule(AnsibleLintRule):
    """Email addresses provided to must use valid domains"""

    id : str = ID
    shortdesc: str = "Email Address Validation"
    description: str = DESC
    severity = "VERY_HIGH"
    tags = ["email", "customer"]
    version_changed = "5.0.11"

    fields_to_check = [
        "bcc",
        "cc",
        "to"
    ]

    def allowed_email_domains(self):
        allowed = self.get_config(C_WHITELIST_EMAIL_DOMAINS)
        if allowed:
            return frozenset(allowed)
        
        return WHITELIST_EMAIL_DOMAINS
    

    def allowedemail(
        self,
        checkemail
    ) -> bool:
        matches = re.search("^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$", checkemail)
        print(matches)
        if matches is None or matches.group(1) is None:
            return False
        domain = matches.group(1)
        if domain in self.allowed_email_domains():
            return True
        return False

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | str:
        if task["action"]["__ansible_module__"] == "community.general.mail" or task["action"]["__ansible_module__"] == "mail":
            checkemails = []
            invalidemails = []
            for field_to_check in self.fields_to_check:
                value = task["action"].get(field_to_check)
                if value is not None:
                    checkemails.append(value)
                    
            for checkemail in checkemails:
                if not self.allowedemail(checkemail):
                    invalidemails.append(checkemail)

            if len(invalidemails) > 0:
                return "The following emails reference invalid domains: " + ", ".join(invalidemails)

    