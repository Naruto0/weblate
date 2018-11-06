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
from weblate.trans.models.unit import Unit
from weblate.trans.models.suggestion import Suggestion
from weblate.trans.models.comment import Comment

from weblate.accounts.notifications import notify_new_translation
from weblate.accounts.notifications import notify_new_suggestion
from weblate.accounts.notifications import notify_new_comment


@receiver(post_save, sender=Unit)
def new_translation_trigger(sender, **kwargs):
    # models.unit.py
    # Notify subscribed users about new translation
    # unit_post_save.send(sender=self.__class__, unit=self, user=user)
    # from weblate.accounts.notifications import notify_new_translation
    # notify_new_translation(self, self.old_unit, user)
    notify_new_translation(sender, sender.old_unit, Change.user)


@receiver(post_save, sender=Suggestion)
def new_suggestion_trigger(sender, **kwargs):
    # models.suggestion.py
    # from weblate.accounts.notifications import notify_new_suggestion
    # notify_new_suggestion(unit, suggestion, user)
    notify_new_suggestion(Change.unit, sender, Change.user)


@receiver(post_save, sender=Comment)
def new_comment_trigger(sender, **kwargs):
    # Notify subscribed users
    #from weblate.accounts.notifications import notify_new_comment
    #notify_new_comment(
    #    unit,
    #    new_comment,
    #    user,
    #    unit.translation.component.report_source_bugs
    #)
    notify_new_comment(Change.unit,
        sender.new_comment, Change.unit, Change.user, Change.unit.translation.component.report_source_bugs)
