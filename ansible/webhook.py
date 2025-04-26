# -*- coding: utf-8 -*-

# Ansible webhook callback plugin

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: webhook
    type: notification
    short_description: Sends playbook results to a webhook
    version_added: "2.0"
    description:
        - This callback plugin sends a summary of the playbook execution to a specified webhook URL.
    options:
      url:
        description: The URL endpoint to send the webhook POST request to.
        required: True
        env:
          - name: ANSIBLE_CALLBACK_WEBHOOK_URL
        ini:
          - section: callback_webhook
            key: url
      http_method:
        description: The HTTP method to use for the webhook request.
        default: 'POST'
        env:
          - name: ANSIBLE_CALLBACK_WEBHOOK_METHOD
        ini:
          - section: callback_webhook
            key: http_method
      headers:
        description: Dictionary of HTTP headers to send with the request (provided as a JSON string in ansible.cfg).
        type: string
        default: '{"Content-Type": "application/json"}'
        env:
          - name: ANSIBLE_CALLBACK_WEBHOOK_HEADERS
        ini:
          - section: callback_webhook
            key: headers
      body_format:
        description: Format of the request body. Currently only 'json' is supported.
        default: 'json'
        env:
          - name: ANSIBLE_CALLBACK_WEBHOOK_BODY_FORMAT
        ini:
          - section: callback_webhook
            key: body_format
      timeout:
        description: Connection timeout in seconds for the webhook request.
        type: int
        default: 10
        env:
            - name: ANSIBLE_CALLBACK_WEBHOOK_TIMEOUT
        ini:
            - section: callback_webhook
              key: timeout
    requirements:
        - python requests library (pip install requests)
'''

import json
import os
import time

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display

# Get the playbook file name (if possible)
# Ansible does not pass the playbook object directly to v2_playbook_on_stats,
# so we try to get it from environment variables or CLI arguments,
# which may not always be reliable.
try:
    from ansible import context
    playbook_path = context.CLIARGS.get('args')[0] if context.CLIARGS.get('args') else 'Unknown Playbook'
except Exception:
    playbook_path = 'Unknown Playbook'


display = Display()

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification' # Plugin type - notification
    CALLBACK_NAME = 'webhook'      # Name by which we will call the plugin
    CALLBACK_NEEDS_ENABLED = True  # Indicates that the plugin needs to be explicitly enabled

    def __init__(self):
        super(CallbackModule, self).__init__()

        self.playbook_name = os.path.basename(playbook_path)
        self.start_time = time.time()

        if not HAS_REQUESTS:
            self.disabled = True
            display.warning("The requests python library is required for the webhook callback plugin. (pip install requests)")

        # Initialize the requests session for connection reuse
        self.session = requests.Session()


    # Method for setting options from ansible.cfg or environment variables
    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        self.webhook_url = self.get_option('url')
        self.webhook_method = self.get_option('http_method').upper()
        self.webhook_headers = self.get_option('headers') # Should be a dict
        self.webhook_body_format = self.get_option('body_format').lower()
        self.timeout = self.get_option('timeout')

        # Check for the required parameter
        if not self.webhook_url:
             self.disabled = True
             display.error("Webhook URL is not defined in ansible.cfg or environment variables for the webhook callback.")

        # Validate headers (must be a dictionary)
        if not isinstance(self.webhook_headers, dict):
            try:
                # Attempt to parse as a JSON string if passed as a string in ini
                self.webhook_headers = json.loads(self.webhook_headers)
                if not isinstance(self.webhook_headers, dict):
                    raise ValueError("Headers must be a dictionary.")
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                 self.disabled = True
                 display.error(f"Invalid format for webhook headers: {self.webhook_headers}. Must be a valid dictionary or JSON string representing a dictionary. Error: {e}")


    # This method is called at the very end of the playbook execution
    def v2_playbook_on_stats(self, stats):
        if self.disabled:
            return

        end_time = time.time()
        duration = round(end_time - self.start_time, 2)

        summary = {}
        status = 'success' # Initially considered successful

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s
            # If there are errors or unreachable hosts, change the status
            if s['failures'] > 0 or s['unreachable'] > 0:
                status = 'failed'

        payload = {
            'playbook': self.playbook_name,
            'status': status,
            'duration_seconds': duration,
            'summary': summary,
            'custom_stats': stats.custom # Add custom statistics, if any
        }

        try:
            if self.webhook_body_format == 'json':
                data_to_send = json.dumps(payload)
                # Make sure the Content-Type is correct for JSON
                if 'Content-Type' not in self.webhook_headers:
                    self.webhook_headers['Content-Type'] = 'application/json'
            else:
                # You can add support for other formats (e.g., form-encoded) if needed
                display.warning(f"Unsupported body_format '{self.webhook_body_format}'. Defaulting to JSON.")
                data_to_send = json.dumps(payload)
                self.webhook_headers['Content-Type'] = 'application/json'


            display.v(f"Webhook: Sending {self.webhook_method} request to {self.webhook_url} with data: {data_to_send}")

            response = self.session.request(
                method=self.webhook_method,
                url=self.webhook_url,
                headers=self.webhook_headers,
                data=data_to_send,
                timeout=self.timeout
            )

            # Check the response status
            response.raise_for_status() # Will raise an exception for 4xx/5xx codes

            display.vv(f"Webhook notification sent successfully to {self.webhook_url}. Status: {response.status_code}. Response: {response.text[:200]}...") # Show part of the response with high verbosity

        except requests.exceptions.RequestException as e:
            display.error(f"Failed to send webhook notification to {self.webhook_url}. Error: {e}")
        except Exception as e:
            # Catch other possible errors (e.g., when forming JSON)
             display.error(f"An unexpected error occurred in the webhook callback plugin: {e}")
