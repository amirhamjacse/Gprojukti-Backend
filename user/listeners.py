from drf_user_activity_tracker import ACTIVITY_TRACKER_SIGNAL

def listener_one(sender, **kwargs):
    print(kwargs)

def listener_two(sender, **kwargs):
    print(kwargs)
