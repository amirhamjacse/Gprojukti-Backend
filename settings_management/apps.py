from django.apps import AppConfig


class SettingsManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings_management'
    
    # def ready(self):
    #     # Schedule task to run at 06:00 PM every day
    #     schedule(
    #         'myapp.tasks.print_current_time',
    #         name='Print Time Daily at 06:00 PM',
    #         schedule_type=Schedule.DAILY,
    #         next_run=datetime.datetime.combine(datetime.date.today(), datetime.time(18, 0)),
    #     )
