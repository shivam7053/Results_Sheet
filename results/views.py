# results/views.py

from django.shortcuts import render
from .models import StudentResult

def result_list(request):
    # Get all results
    results = StudentResult.objects.all()

    # Get user input for filtering
    college_filter = request.GET.get('college')
    batch_filter = request.GET.get('batch')
    semester_filter = request.GET.get('semester')
    
    # Apply filters if they exist
    if college_filter:
        results = results.filter(college_name=college_filter)
    if batch_filter:
        results = results.filter(batch=batch_filter)
    if semester_filter:
        results = results.filter(semester=semester_filter)

    # Create a dictionary to store unique results by university roll no
    unique_results = {}
    for result in results:
        if result.university_roll_no not in unique_results:
            unique_results[result.university_roll_no] = result  # Store the full object

    # Determine which average to show
    for result in unique_results.values():
        if semester_filter:
            # Show the average for the specific semester
            result.semester_avg = getattr(result, f'subject_{semester_filter}', result.overall_avg)
        else:
            # Show the overall average
            result.semester_avg = result.overall_avg

    return render(request, 'results/result_list.html', {
        'results': unique_results.values(),
        'semester_filter': semester_filter
    })



# results/views.py
from django.shortcuts import render
from .models import StudentResult
import matplotlib.pyplot as plt
import io
import base64

def student_performance(request):
    performance_data = None
    subject_marks_data = None
    pie_chart_data = None
    comparison_data = None
    roll_no = request.GET.get('roll_no', '')

    if roll_no:
        # Fetch the results for the given university roll number
        results = StudentResult.objects.filter(university_roll_no=roll_no)

        # Prepare data for visualization
        if results.exists():
            semesters = [result.semester for result in results]
            overall_averages = [result.overall_avg for result in results]
            semester_averages = [result.semester_avg for result in results]
            latest_result = results.last()  # Get the latest semester results

            # 1. Create Line Chart for Performance
            plt.figure(figsize=(10, 5))
            plt.plot(semesters, overall_averages, marker='o', label='Overall Average')
            plt.plot(semesters, semester_averages, marker='o', linestyle='--', label='Semester Average')
            plt.title('Performance Overview')
            plt.xlabel('Semesters')
            plt.ylabel('Averages')
            plt.xticks(semesters)
            plt.legend()
            plt.grid()
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            performance_data = base64.b64encode(buf.read()).decode('utf-8')

            # 2. Create Bar Chart for Subject Marks
            subjects = ['subject_1', 'subject_2', 'subject_3', 'subject_4', 'subject_5', 'subject_6']
            subject_marks = [getattr(latest_result, subject) for subject in subjects]

            plt.figure(figsize=(10, 5))
            plt.bar(subjects, subject_marks, color='skyblue')
            plt.title('Subject Marks for Latest Semester')
            plt.xlabel('Subjects')
            plt.ylabel('Marks')
            plt.xticks(rotation=45)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            subject_marks_data = base64.b64encode(buf.read()).decode('utf-8')

            # 3. Create Pie Chart for Overall Performance
            total_marks = sum(subject_marks)
            pie_chart_labels = subjects
            pie_chart_sizes = subject_marks
            plt.figure(figsize=(8, 8))
            plt.pie(pie_chart_sizes, labels=pie_chart_labels, autopct='%1.1f%%', startangle=140)
            plt.title('Overall Performance Distribution')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            pie_chart_data = base64.b64encode(buf.read()).decode('utf-8')

            # 4. Create Bar Chart for Average Performance Comparison
            plt.figure(figsize=(10, 5))
            labels = ['Overall Average'] + [f'Semester {sem}' for sem in semesters]
            comparison_values = [latest_result.overall_avg] + semester_averages
            plt.bar(labels, comparison_values, color='lightgreen')
            plt.title('Average Performance Comparison')
            plt.ylabel('Averages')
            plt.xticks(rotation=45)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            comparison_data = base64.b64encode(buf.read()).decode('utf-8')

    return render(request, 'results/student_performance.html', {
        'performance_data': performance_data,
        'roll_no': roll_no,
        'subject_marks_data': subject_marks_data,
        'pie_chart_data': pie_chart_data,
        'comparison_data': comparison_data,
    })
