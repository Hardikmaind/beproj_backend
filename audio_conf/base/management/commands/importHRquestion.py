# your_app/management/commands/import_questions.py
import csv
from django.core.management.base import BaseCommand
from ...models import HrinterviewQuestions, TechnicalinterviewQuestions  # Use absolute import

class Command(BaseCommand):
    help = 'Import questions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file', default='audio_conf/base/dataset.csv')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if exists

            for row in reader:
                quesionlist = row[0]  # Adjust column index as needed
                HrinterviewQuestions.objects.create(quesionlist=quesionlist)
                self.stdout.write(self.style.SUCCESS(f'Successfully created question: {quesionlist}'))
        # HrinterviewQuestions.objects.all().delete()           //this is used to delete the all the rows and empty
        
        
# python manage.py importHRquestion .\base\dataset.csv          //use this command to do the filling the database in root directory 
    
                
                