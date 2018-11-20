from weblate.accounts.models import Profile
from weblate.trans.models import Change

MAP = {
    Change.ACTION_SUGGESTION: 'subscribe_new_suggestion',
    Change.ACTION_COMMENT: 'subscribe_new_comment',
    Change.ACTION_NEW: 'subscribe_any_translation',
    Change.ACTION_NEW_SOURCE: 'subscribe_new_string',
    Change.ACTION_FAILED_MERGE: 'subscribe_merge_failure',
}


class ChangeSignal():
    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.kwargs = kwargs

    def __repr__(self):
        return str(self.instance.action) + self.instance.target


class NotificationQueue():
    def __init__(self):
        self.array = []

    def array(self):
        return self.array

    def clear(self):
        self.array.clear()


queue = NotificationQueue()


def enqueue_change(instance, **kwargs):
    queue.array.append(ChangeSignal(instance, **kwargs))
    print(queue.array)
    subscriptions = Profile.objects.subscribed_only_digest()
    for profile in subscriptions:
        print getattr(profile, 'subscribe_new_suggestion')


def process_digest(queue):
    subscriptions = Profile.objects.subscribed_only_digest()
    for profile in subscriptions:
        print getattr(profile, 'subscribe_new_suggestion')
