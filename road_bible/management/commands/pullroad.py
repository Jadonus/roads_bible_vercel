import json
import os
from django.core.management.base import BaseCommand
from road_bible.models import CustomRoads
import subprocess


class Command(BaseCommand):
    help = 'Pull a road and download a JSON file with verses.'

    def add_arguments(self, parser):
        parser.add_argument('roadname', type=str,
                            help='Name of the road to pull')
        parser.add_argument('user', type=str,
                            help='Username of the road.')

    def handle(self, *args, **options):
        roadname = options['roadname']
        user = options['user']
        self.stdout.write(f'\033[34mPulling {roadname} from {user}\033[39m')

        try:
            ob = CustomRoads.objects.get(title=roadname, creator=user)
            verses = ob.verses

            if verses:
                titlee = ob.title

                title = titlee.replace(" ", "_")
                json_data = json.dumps(verses, indent=4)

                # Define the filename based on the title
                file_name = f'{title}.json'

                # Specify the directory where you want to save the file
                # Replace with the actual directory path
                save_directory = 'static/roads'

                file_path = os.path.join(save_directory, file_name)

                # Write the JSON data to the file
                with open(file_path, 'w') as file:
                    file.write(json_data)

                self.stdout.write(
                    f'\033[32m✅ Road Pulled, Syncing... {file_name}\033[39m')

                subprocess.run(['git', 'add', '.'])
                subprocess.run(['git', 'commit', '-m', title])

                subprocess.run(['git', 'push'])

                self.stdout.write(
                    f'\033[32m🚀 Full Success {file_name} Uploaded.\033[39m')
            else:
                self.stdout.write(f'\033[31mNo verses found!\033[39m')

        except CustomRoads.DoesNotExist:
            self.stdout.write(f'\033[31mThis Does Not Exist!\033[39m')
