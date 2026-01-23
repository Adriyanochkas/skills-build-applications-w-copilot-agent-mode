from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data in the correct order (children before parents)
        for model in [Leaderboard, Activity, Workout]:
            for obj in model.objects.all():
                obj.delete()
        for user in User.objects.all():
            if getattr(user, 'id', None):
                user.delete()
        for team in Team.objects.all():
            if getattr(team, 'id', None):
                team.delete()

        # Create Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create Users
        tony = User.objects.create(email='tony@stark.com', name='Tony Stark', team='marvel')
        steve = User.objects.create(email='steve@rogers.com', name='Steve Rogers', team='marvel')
        bruce = User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team='dc')
        clark = User.objects.create(email='clark@kent.com', name='Clark Kent', team='dc')

        # Create Activities
        Activity.objects.create(user=tony, type='run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, type='swim', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='cycle', duration=60, date=timezone.now().date())
        Activity.objects.create(user=clark, type='fly', duration=120, date=timezone.now().date())

        # Create Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        Workout.objects.create(name='Situps', description='Do 30 situps', suggested_for='dc')

        # Create Leaderboard
        Leaderboard.objects.create(user=tony, points=100, rank=1)
        Leaderboard.objects.create(user=steve, points=80, rank=2)
        Leaderboard.objects.create(user=bruce, points=90, rank=1)
        Leaderboard.objects.create(user=clark, points=70, rank=2)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
