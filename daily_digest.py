from datetime import datetime, timedelta

from weblate.trans.models import Change, Project
from weblate.auth.models import User
from weblate.accounts.models import Profile

MAP = {
    Change.ACTION_SUGGESTION: 'subscribe_new_suggestion',
    Change.ACTION_COMMENT: 'subscribe_new_comment',
    Change.ACTION_NEW: 'subscribe_any_translation',
    Change.ACTION_NEW_SOURCE: 'subscribe_new_string',
    Change.ACTION_FAILED_MERGE: 'subscribe_merge_failure',
}


#YESTERDAY = datetime.now().date() - timedelta(days = 1)
TODAY = datetime.now().date()


def process():
    # yesterday_changes = Change.objects.filter(timestamp = YESTERDAY)
    digest_users= Profile.objects.subscribed_only_digest()
    today_changes= Change.objects.filter(timestamp= TODAY)

    for user in digest_users:
        if digest_users.subscriptions 

    # for each change
    affected_projects= today_changes.prefetch('project_id')