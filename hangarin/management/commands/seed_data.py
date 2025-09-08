from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from hangarin.models import Task, SubTask, Note, Category, Priority

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]

        for c in categories:
            Category.objects.get_or_create(name=c)
        for p in priorities:
            Priority.objects.get_or_create(name=p)

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=random.choice(["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                category=Category.objects.order_by("?").first(),
                priority=Priority.objects.order_by("?").first(),
            )
            for _ in range(2):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=random.choice(["Pending", "In Progress", "Completed"]),
                )
            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )
        self.stdout.write(self.style.SUCCESS("Database seeded with fake data!"))
