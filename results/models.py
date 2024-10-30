# results/models.py

from django.db import models

class StudentResult(models.Model):
    university_roll_no = models.CharField(max_length=10)
    college_name = models.CharField(max_length=100)
    batch = models.IntegerField()
    semester = models.IntegerField()
    subject_1 = models.FloatField()
    subject_2 = models.FloatField()
    subject_3 = models.FloatField()
    subject_4 = models.FloatField()
    subject_5 = models.FloatField()
    subject_6 = models.FloatField()
    semester_avg = models.FloatField()
    overall_avg = models.FloatField()

    def __str__(self):
        return f"{self.university_roll_no} - Batch: {self.batch} - Overall Avg: {self.overall_avg}"
