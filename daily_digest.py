from datetime import datetime, timedelta

from weblate.trans.models import Change
from weblate.accounts.models import Profile
from django.template.loader import render_to_string


# map <change.action> to <Profile> model subscription field
# TODO: Once changes for below ins implemented add:

# 'subscribe_new_contributor': None,
# 'subscribe_new_language': None
SUBSCRIPTION_MAP = {
    'subscribe_any_translation': Change.ACTION_NEW,
    'subscribe_new_string': Change.ACTION_NEW_SOURCE,
    'subscribe_new_suggestion': Change.ACTION_SUGGESTION,
    'subscribe_new_comment': Change.ACTION_COMMENT,
    'subscribe_merge_failure': Change.ACTION_FAILED_MERGE,
}


# define date for chage extracion
YESTERDAY = datetime.now().date() - timedelta(days=1)
TODAY = datetime.now().date()


# process daily digest
def process_digest():
    """ Process changes from yesterday picking changes based on
    Profile subscriptions."""
    digest_profiles = Profile.objects.subscribed_only_digest()
    for profile in digest_profiles:
        profile_sub_proj = profile.subscriptions.all()
        profile_subs = []
        email = []

        # If the action is not mapped it won't get through filter
        for _ in profile.get_active_subs():
            try:
                profile_subs.append(SUBSCRIPTION_MAP[_])
            except KeyError:
                pass

        print 'User:'
        print profile
        print '===================='
        print 'subscriptions:'
        print profile.get_active_subs()

        # for each project in notification subscribed projects
        for sub_project in profile_sub_proj:

            print 'Project:'
            print sub_project
            print '________________'
            # 
            today_changes = Change.objects.filter(
                timestamp__date=TODAY,
                project_id=sub_project,
                action__in=profile_subs,
            ).exclude(
                user_id=profile.user_id
            )

            #if today_changes:
            #    compose(today_changes)

            for change in today_changes:
                print change

    # for each change
    # affected_projects= today_changes.prefetch('project_id')
