from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt 

# Create a stud_dict having student_id as keys and course_id,marks as list of lists.
# Create a course_dict having course_id as keys and the obtained marks in the course as a list.
(stud_dict,course_dict) = ({},{})
def initialize_data():
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
initialize_data()

app = Flask(__name__)



@app.route("/", methods=["GET","POST"])
def main():
    try:
        if request.method == 'GET':
            return render_template('enter_details.html')

        elif request.method=='POST':
            selected_id = request.form.get('ID')
            id_val= request.form["id_value"]
            if selected_id == 'student_id':
                req_data = stud_dict[id_val]
                sum=0
                for val in req_data:
                    sum += int(val[1])
                return render_template('student_details.html',my_data=req_data,student_id_data=id_val,total_marks_data=sum)
            elif selected_id == 'course_id':
                req_marks = course_dict[id_val]
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
                plt.savefig('static/image.png')
                return render_template('course_details.html',average_marks=avg_marks,maximum_marks=maxi)
    except:
        return render_template('wrong_inp.html')



if __name__=='__main__':
    #function call
    app.debug=True
    app.run()
    main()

