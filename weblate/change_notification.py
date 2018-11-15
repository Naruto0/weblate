
class ChangeSignal():
    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.kwargs = kwargs


class NotificationQueue():
    def __init__(self):
        self.array = []

    def __repr__(self):
        return self.array


queue = NotificationQueue()


def enqueue_change(instance, **kwargs):
    queue.array.append(ChangeSignal(instance, **kwargs))
