import sys
import matplotlib.pyplot as plt
from jinja2 import Template


# Create a stud_dict having student_id as keys and course_id,marks as list of lists.
# Create a course_dict having course_id as keys and the obtained marks in the course as a list.
(stud_dict,course_dict) = ({},{})

# Open the data.csv file
data_file = open("data.csv","r")

#Read Heading first.
heading = data_file.readline()

# Read the actual data line by line and store it in a list.
data = data_file.readline().rstrip().split(', ') # There is one space after comma.

# Iterate till there is no data left.
# data[0] = Student_id, data[1] = Course_id, data[2] = Marks
while(data!=['']):
    # Creating Student_dictionary first
    if data[0] not in stud_dict.keys():
        stud_dict[data[0]] = [[data[1],data[2]]]
    else:
        stud_dict[data[0]].append([data[1],data[2]])
    
    # Creating Course_dictionar.
    if data[1] not in course_dict.keys():
        course_dict[data[1]] = [data[2]]
    else:
        course_dict[data[1]].append(data[2])
    
    # Readline for next Iteration.
    data = data_file.readline().rstrip().split(', ') # There is one space after comma.

# Close the file after processing the data.
data_file.close()

# Student Template
Student_Template='''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Student Data</title>
    </head>
    <body>
        <h1>Student Details</h1>
        <table border=1px>
            <tr>
                <th>Student ID</th>
                <th>Course ID</th>
                <th>Marks</th>
            </tr>
            {% for elem in my_data %}
            <tr>
                <td>{{ sec_para }}</td>
                <td>{{ elem[0] }}</td>
                <td>{{ elem[1] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2" style="text-align: center">Total Marks</td>
                <td>{{ tot_marks }}</td>
            </tr>
        </table>
    </body>
</html>
'''
#Course Template
Course_Template = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Course Data</title>
    </head>
    <body>
        <h1>Course Details</h1>
        <table border=1px solid black>
            <thead>
                <tr>
                    <th>Average Marks</th>
                    <th>Maximum Marks</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{avg_marks}}</td>
                    <td>{{max_marks}}</td>
                </tr>
            </tbody>
        </table>
        <img src="image.png">
    </body>
</html>
'''

#Wrong Input Template
Wrong_Inp_Template = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>Something Went Wrong</title>
    </head>
    <body>
        <h1>Wrong Inputs</h1>
        <p>Something went wrong</p>
    </body>
</html>
'''

# Store Input arguments/parameters.
first_para = sys.argv[1]
sec_para = sys.argv[2]

try:
    #Check for input id type
    if first_para == '-s':

        # Storing the req_data to calculate the total marks
        req_data = stud_dict[sec_para]
        sum=0
        for val in req_data:
            sum += int(val[1])

        #Render the template
        template = Template(Student_Template)
        content = template.render(my_data=req_data,sec_para=sec_para,tot_marks=sum)
        
        #Save the html output file
        output_html = open('output.html', 'w')
        output_html.write(content)
        output_html.close()
    
    #Check for input id type
    elif first_para == '-c':
        
        # Storing the req_marks to calculate the avg_marks, max_marks and plot the histogram.
        req_marks = course_dict[sec_para]
        count = 0
        sum=0
        maxi=float(req_marks[0])
        for val in req_marks:
            count += 1
            sum += float(val)
            if maxi < float(val):
                maxi = float(val)
        avg_marks = sum/count
        
        # Create Histogram plot
        plt.hist(req_marks,histtype="bar",rwidth=0.7)

        plt.xlabel("Marks")
        plt.ylabel("Frequency")

        #Save plot as png file
        plt.savefig('image.png')

        #Render the template
        template = Template(Course_Template)
        content = template.render(avg_marks=avg_marks,max_marks=maxi)

        #Save the html output file
        output_html = open('output.html', 'w')
        output_html.write(content)
        output_html.close()
    
    # Exception case for wrong id input  type.
    else:
        #Render the template
        template = Template(Wrong_Inp_Template)
        content = template.render()
        
        #Save the html output file
        output_html = open('output.html', 'w')
        output_html.write(content)
        output_html.close()

except:

    #Render the template
    template = Template(Wrong_Inp_Template)
    content = template.render()

    #Save the html output file
    output_html = open('output.html', 'w')
    output_html.write(content)
    output_html.close()



