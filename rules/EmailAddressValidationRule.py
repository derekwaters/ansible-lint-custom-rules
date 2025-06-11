"""Implementation of email-address-validation rule."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ansiblelint.constants import FILENAME_KEY, LINE_NUMBER_KEY
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task, get_first_cmd_arg

import re

if TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable


class EmailAddressValidationRule(AnsibleLintRule):
    """Email addresses provided to the If any task uses:
- The `community.general.mail` module
- A `uri` module or raw `telnet` to port 25 (SMTP)

Then the recipient email address must be in the `@customer.com.au` domain. This rule ensures email notifications do not leak externally and requires regex validation on `to:` or `rcpt_to:` fields.

    ."""

    id = "email-address-validation"
    description = (
        "Sending email should only use valid email addresses"
    )
    severity = "VERY_HIGH"
    tags = ["email", "customer"]
    version_changed = "5.0.11"

    allowed_email_domains = [
        "customer.com.au",
        "cust.com.au"
    ]

    def allowedemail(
        self,
        checkemail
    ) -> bool:
        matches = re.search("^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$". checkemail)
        if matches is None:
            return False
        domain = matches.group()
        if domain in self.allowed_email_domains:
            return True
        return False

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | str:
        if task["action"]["__ansible_module__"] == "mail":
            checkemails = []
            invalidemails = []
            checkemails.append(task["action"].get("bcc"))
            checkemails.append(task["action"].get("cc"))
            checkemails.append(task["action"].get("to"))
            for checkemail in checkemails:
                if not self.allowedemail(checkemail):
                    invalidemails.push(checkemail)

            if len(invalidemails) > 0:
                return False
        return True
    