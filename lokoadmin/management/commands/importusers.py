import uuid

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from user_profiles.models import UserType, ParentChildren, ChildProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.wipe_users()
        self.parse_file_of_users()

    def wipe_users(self):
        User.objects.exclude(username='oh').delete()
        UserType.objects.filter(user_type__in=[1, 2]).delete()
        ParentChildren.objects.all().delete()
        ChildProfile.objects.all().delete()

    def parse_file_of_users(self):
        def pairwise(iterable):
            """s -> (s0, s1, s02), (s3, s4, s5), ..."""
            a = iter(iterable)
            return zip(a, a, a)

        output = open('users.output', 'w')
        with open('users.import') as file:
            for line in file:
                line = line.split()
                name, surname, email, children = line[0], line[1], line[2], line[3:]
                username = email.split('@')[0]
                u = User.objects.create(
                    first_name=name,
                    last_name=surname,
                    username=username,
                    email=email,
                )

                password = str(uuid.uuid4()).upper()[0:8]
                if username == 'kostolna':
                    print(password)
                u.set_password(password)
                u.save()

                UserType.objects.create(
                    user=u,
                    user_type=2,
                )
                print('{}:{}'.format(username, password), file=output)
                for child_info in pairwise(children):
                    last_name = child_info[0]
                    first_name = child_info[1]
                    username = child_info[1] + '-' + child_info[0]
                    password = str(uuid.uuid4()).upper()[0:8]

                    year = child_info[2]
                    if ChildProfile.objects.filter(user__username=username).exists():
                        ch = ChildProfile.objects.get(user__username=username)
                    else:
                        child = User.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                        )
                        child.set_password(password)
                        child.save()
                        ch = ChildProfile.objects.create(
                            user=child,
                            birthday='{}-01-01'.format(year),
                            member_since=timezone.now(),
                        )
                        UserType.objects.create(
                            user=child,
                            user_type=1,
                        )
                    if not ParentChildren.objects.filter(user=u).exists():
                        ParentChildren.objects.create(
                            user=u
                        )
                    u.parentchildren.children.add(ch)
                    print('    - {}:{}'.format(username, password), file=output)

        output.close()
