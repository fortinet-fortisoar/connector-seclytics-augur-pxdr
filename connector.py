"""Main connector object that contains actions."""
from connectors.core.connector import Connector, get_logger # pylint: disable=E0401
from django.utils.module_loading import import_string # pylint: disable=E0401
from .builtins import supported_operations  # pylint: disable=E0402
from .constants import LOGGER_NAME          # pylint: disable=E0402

logger = get_logger(LOGGER_NAME)


class SeclyticsAugur(Connector):
    """Main connector object that contains actions."""

    def dev_execute(self, config, operation, params):
        """Import the function on every invocation for development ONLY."""
        parent_path = __name__.split('.')[:-1]
        parent_path.extend([operation, operation])
        func = import_string('.'.join(parent_path))
        return func(config, params)

    def execute(self, config, operation, params, **kwargs):
        """Execute various actions of the connector."""
        # Call dev_execute from the 'execute' function if you are doing very
        # frequent changes to the connector code and changes don't reflect
        # without a service restart.
        # return self.dev_execute(config, operation, params)
        return supported_operations.get(operation)(config, params)

    def check_health(self, config=None):
        """Check the connectivity to Seclytics API."""
        return supported_operations.get('check_api_health')(config)
