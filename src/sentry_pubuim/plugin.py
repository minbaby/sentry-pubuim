"""
sentry_pubuim.plugin
~~~~~~~~~~~~~~~~~~~

:license: BSD, see LICENSE for more details.
"""
import sentry_pubuim
import logging

from django import forms

from sentry import http
from sentry.plugins.bases import notify
from sentry.utils import json


# warning|info|primary|error|muted|success
LEVEL_TO_COLOR = {
    'debug': 'muted',
    'info': 'info',
    'warning': 'warning',
    'error': 'error',
    'fatal': 'primary',
}

DEFAULT_IMG = 'https://raw.githubusercontent.com/minbaby/sentry-pubuim/master/idxdmy.jpeg'


log = logging.getLogger('test1')


def get_project_full_name(project):
    if project.team.name not in project.name:
        return '%s %s' % (project.team.name, project.name)
    return project.name


class PubuimOptionsForm(notify.NotificationConfigurationForm):
    webhook = forms.URLField(
        help_text='Your custom Pubuim webhook URL',
        widget=forms.URLInput(attrs={'class': 'span8'})
    )
    username = forms.CharField(
        label='Bot Name',
        help_text='The name that will be displayed by your bot messages.',
        widget=forms.TextInput(attrs={'class': 'span8'}),
        initial='Sentry',
        required=False
    )
    icon_url = forms.URLField(
        label='Icon URL',
        help_text='The url of the icon to appear beside your bot (32px png), '
                  'leave empty for none.<br />You may use '
                  'https://raw.githubusercontent.com/minbaby/sentry-pubuim/master/idxdmy.jpeg',
        widget=forms.URLInput(attrs={'class': 'span8'}),
        required=False
    )


class PubuimPlugin(notify.NotificationPlugin):
    author = 'Minbaby zhang'
    author_url = 'https://github.com/minbaby'
    resource_links = (
        ('Comppnay Link', 'http://www.behinders.com'),
        ('Blog Link', 'https://blog.891125.com')
    )

    title = 'Pubu.im'
    slug = 'pubuim'
    description = 'Post notifications to a pubuim channel.'
    conf_key = 'pubuim'
    version = sentry_pubuim.VERSION
    project_conf_form = PubuimOptionsForm

    def is_configured(self, project):
        return all((self.get_option(k, project) for k in ('webhook',)))

    def color_for_group(self, group):
        return LEVEL_TO_COLOR.get(group.get_level_display(), 'error')

    def notify(self, notification):
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return

        webhook = self.get_option('webhook', project)
        username = self.get_option('username', project).strip()
        icon_url = self.get_option('icon_url', project)

        title = group.message_short.encode('utf-8')
        project_name = get_project_full_name(project).encode('utf-8')

        payload = {
            "text": '[%s] %s' % (project_name, title),
            "attachments": [{
                "title": title,
                "description": title,
                "url": group.get_absolute_url(),
                "color": self.color_for_group(group)
            }],
            "displayUser": {
                "name": username.encode('utf-8'),
                "avatarUrl": ""
            }
        }

        payload['displayUser']['avatarUrl'] = icon_url if icon_url else DEFAULT_IMG

        values = json.dumps(payload)

        # Apparently we've stored some bad data from before we used `URLField`.
        webhook = webhook.strip(' ')
        return http.safe_urlopen(webhook, method='POST', data=values, headers={"Content-Type":"application/json"})
