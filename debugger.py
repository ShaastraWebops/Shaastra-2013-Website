#!/usr/bin/python
# -*- coding: utf-8 -*-
import local_settings
from local_settings import *

if DEBUG:
    import sys
    import os

    DEBUG_DIR = '/home/shaastra/django-debug-toolbar/'

    if not DEBUG_DIR in sys.path:
        sys.path.append(DEBUG_DIR)

    TEMPLATE_DIRS = TEMPLATE_DIRS + (DEBUG_DIR
            + 'debug_toolbar/templates', )

    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES \
        + ('debug_toolbar.middleware.DebugToolbarMiddleware', )

    # Kabhi = 117.192.179.42
    # Serup = 117.193.5.17
    # mani = 117.193.37.22
    # varshaa = 203.199.213.3

    # Please add your name and ip as comment before adding to this tuple

    INTERNAL_IPS = ('127.0.0.1', '117.192.179.42', '117.193.5.17',
                    '117.193.37.22', '203.199.213.3')

    DATABASE_ENGINE = 'mysql'
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
        )
