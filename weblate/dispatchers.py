# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from django.dispatch import receiver
from django.db.models.signals import post_save

from weblate.trans.models import Change

from weblate.accounts.notifications import (
    notify_new_translation,
    notify_new_string,
    notify_new_suggestion,
    notify_new_comment,
    notify_merge_failure
)
from weblate.change_notification import enqueue_change


@receiver(post_save, sender=Change)
def instant_change_dispatcher(sender, instance, **kwargs):
    # handle default non digest notifications
    if instance.action == Change.ACTION_SUGGESTION:
        notify_new_suggestion(
            instance.unit,
            instance.target,
            instance.user
        )
    elif instance.action == Change.ACTION_COMMENT:
        notify_new_comment(
            instance.unit,
            instance.translation,
            instance.user,
            instance.component.report_source_bugs
        )
    elif instance.action == Change.ACTION_NEW:
        notify_new_translation(
            instance,
            instance.unit.old_unit,
            instance.user
        )
    elif instance.action == Change.ACTION_NEW_SOURCE:
        notify_new_string(
            instance,
            instance.user
        )
    elif instance.action == Change.ACTION_FAILED_MERGE:
        notify_merge_failure(
            instance.component,
            instance.error,
            instance.status
        )

'''
@receiver(post_save, sender=Change)
def digest_dispatcher(instance, **kwargs):
    # handle digest changes
    enqueue_change(instance, **kwargs)
'''