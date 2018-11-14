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

from weblate.accounts.notifications import notify_new_translation
from weblate.accounts.notifications import notify_new_suggestion
from weblate.accounts.notifications import notify_new_comment


@receiver(post_save, sender=Change)
def change_dispatcher(sender, instance, **kwargs):
    if instance.action == Change.ACTION_SUGGESTION:
        notify_new_suggestion(
            instance.unit,
            instance.target,
            instance.user
        )
    elif instance.action == Change.ACTION_COMMENT:
        notify_new_comment(
            instance.unit,
            instance.target,
            instance.user,
            instance.component.report_source_bugs
            )
    elif instance.action == Change.ACTION_NEW:
        notify_new_translation(
            instance.translation,
            instance.old_unit,
            instance.user
        )