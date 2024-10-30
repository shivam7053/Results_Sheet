import pandas as pd
from django.core.management.base import BaseCommand
from results.models import StudentResult  # Adjust this to your actual app name
import os

class Command(BaseCommand):
    help = 'Import student results from a CSV file'

    def handle(self, *args, **kwargs):
        # Specify the full path to your CSV file
        csv_file = r'C:\coding\python\django\result\result_proj\results\management\commands\output1.csv'  # Adjust this path as necessary

        # Make sure the file exists
        if not os.path.isfile(csv_file):
            self.stdout.write(self.style.ERROR(f"File '{csv_file}' not found."))
            return

        try:
            data = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR(f"File '{csv_file}' is empty."))
            return
        except pd.errors.ParserError:
            self.stdout.write(self.style.ERROR(f"File '{csv_file}' could not be parsed."))
            return

        for _, row in data.iterrows():
            StudentResult.objects.create(
                university_roll_no=row['University_Roll_No'],
                college_name=row['College_Name'],
                batch=row['Batch'],
                semester=row['Semester'],
                subject_1=row['Subject_1'],
                subject_2=row['Subject_2'],
                subject_3=row['Subject_3'],
                subject_4=row['Subject_4'],
                subject_5=row['Subject_5'],
                subject_6=row['Subject_6'],
                semester_avg=row['Semester_Avg'],
                overall_avg=row['Overall_Avg']
            )
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
