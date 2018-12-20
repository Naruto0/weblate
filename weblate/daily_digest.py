from weblate.trans.models import Change
from weblate.accounts.models import Profile
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# map <change.action> to <Profile> model subscription field
# TODO: Once changes for below ins implemented add:
#   'subscribe_new_contributor': None,
#   'subscribe_new_language': None
SUBSCRIPTION_MAP = {
    'subscribe_any_translation': Change.ACTION_NEW,
    'subscribe_new_string': Change.ACTION_NEW_SOURCE,
    'subscribe_new_suggestion': Change.ACTION_SUGGESTION,
    'subscribe_new_comment': Change.ACTION_COMMENT,
    'subscribe_merge_failure': Change.ACTION_FAILED_MERGE,
}

CHANGE_MAP = {
    Change.ACTION_NEW: 'translation',
    Change.ACTION_NEW_SOURCE: 'string',
    Change.ACTION_SUGGESTION: 'suggestion',
    Change.ACTION_COMMENT: 'comment'
}


# Interval based on Profile.SUBSCRIPTION_TYPES
def process_digest(interval=2):
    """ Process changes from yesterday picking changes based on
    Profile subscriptions."""
    digest_profiles = Profile.objects.subscribed_to_digest(interval)
    for profile in digest_profiles:
        profile_sub_proj = profile.subscriptions.all()
        profile_subs = []

        # If the action is not mapped it won't get through filter
        for x in profile.get_digest_subs(interval):
            try:
                profile_subs.append(SUBSCRIPTION_MAP[x])
            except KeyError:
                pass

        context = {'projects': []}

        # for each project in notification subscribed projects
        for sub_project in profile_sub_proj:

            project = {
                'name': sub_project.name
            }

            proj_changes = Change.objects.digest(
                interval,
                sub_project,
                profile_subs,
                profile.user_id
            )

            changes = []

            for change in proj_changes:
                if change.target:
                    target = change.target
                else:
                    target = None
                # if change.old:
                #     old = change.old
                # else:
                #     old = None
                template = 'mail/digest_{}.html'.format(CHANGE_MAP[change.action])
                changes.append({
                    'change': change,
                    'template': template,
                    'target': target,
                    # 'old': old
                })
            project['changes'] = changes

            context['projects'].append(project)

        # print context

        if interval == 2:
            context['timespan'] = _('day')
        else:
            context['timespan'] = _('week')

        context['site_title'] = settings.SITE_TITLE


        fire_an_email(profile, context)



def fire_an_email(profile, context):
    #print 'sending to {}'.format(profile)
    print render_to_string('mail/digest.html', context)
    print context
    """
    context = {}
    context['timespan'] = 'week'
    context['subject_template'] = 'mail/digest_subject.txt'
    context['translation'] = 'whatever'
    print context
    print render_to_string('mail/digest.html', context)
    """
