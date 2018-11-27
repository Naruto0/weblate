from datetime import datetime, timedelta

from weblate.trans.models import Change, Project
from weblate.auth.models import User
from weblate.accounts.models import Profile

from pprint import pprint

MAP = {
    'subscribe_new_suggestion': Change.ACTION_SUGGESTION,
    'subscribe_new_comment': Change.ACTION_COMMENT,
    'subscribe_any_translation': Change.ACTION_NEW,
    'subscribe_new_string': Change.ACTION_NEW_SOURCE,
    'subscribe_merge_failure': Change.ACTION_FAILED_MERGE
}


YESTERDAY = datetime.now().date() - timedelta(days = 1)
TODAY = datetime.now().date()

def process():
    digest_profiles = Profile.objects.subscribed_only_digest()
    for profile in digest_profiles:
        profile_sub_proj = profile.subscriptions.all()
        profile_subs = []

        for _ in profile.get_active_subs():
            try:
                profile_subs.append(MAP[_])
            except KeyError:
                pass

        print 'User:'
        print profile
        print '===================='
        print 'subscriptions:'
        print profile.get_active_subs()

        for sub_project in profile_sub_proj:

            print 'Project:'
            print sub_project
            print '________________'

            today_changes = Change.objects.filter(
                timestamp__date=TODAY,
                project_id=sub_project,
                action__in=profile_subs
            )
            for change in today_changes.all():
                print change


    # for each change
    # affected_projects= today_changes.prefetch('project_id')
