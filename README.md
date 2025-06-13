# ansible-lint-custom-rules
Custom Ansible-Lint Rules

Two example custom ansible-lint rules:

### EmailAddressValidationRule.py

This rule searches for any tasks using community.general.mail and validates that 
all to / bcc / cc fields contain email addresses with whitelisted domains. This
prevents inadvertent or malicious exfiltration of data from Ansible plays.

### MustIncludeCollectionsRule.py

This rule checks the collections section of a playbook and ensures that a
configured list of collections are included. This allows for the configuration
of a mandatory collection to perform any internal checks required prior to
playbook execution.

Both rules may be enabled / disabled in various ansible-line profiles and
can be configured to specify the whitelist / mandatory collection list as
required.