from datetime import datetime, timedelta

from weblate.trans.models import Change
from weblate.accounts.models import Profile


# map <change.action> to <Profile> model subscription field
SUBSCRIPTION_MAP = {
    'subscribe_new_suggestion': Change.ACTION_SUGGESTION,
    'subscribe_new_comment': Change.ACTION_COMMENT,
    'subscribe_any_translation': Change.ACTION_NEW,
    'subscribe_new_string': Change.ACTION_NEW_SOURCE,
    'subscribe_merge_failure': Change.ACTION_FAILED_MERGE
}


# define date for chage extracion
YESTERDAY = datetime.now().date() - timedelta(days = 1)
TODAY = datetime.now().date()


# process daily digest
def process():
    digest_profiles = Profile.objects.subscribed_only_digest()
    for profile in digest_profiles:
        profile_sub_proj = profile.subscriptions.all()
        profile_subs = []
        email = []

        # use the above mapping for filtering the changes regarding this profile
        # subscriptions
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

        for sub_project in profile_sub_proj:

            print 'Project:'
            print sub_project
            print '________________'

            today_changes = Change.objects.filter(
                timestamp__date=TODAY,
                project_id=sub_project,
                action__in=profile_subs
            )

            if today_changes:
                email.append(Project)

            for change in today_changes.all():
                print change


    # for each change
    # affected_projects= today_changes.prefetch('project_id')
