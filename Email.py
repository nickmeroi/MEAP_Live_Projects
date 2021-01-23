import operator
from itertools import chain, combinations
import random
import smtplib
import csv
from pprint import pprint


def inspect_file(file):

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader, 1):
            print(f'Row_{i}: {row}')


def save_students_data(file):

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # the key is the student's email
        students_data = {row[0]: {'last_name': row[1],
                                  'first_name': row[2],
                                  'p1_score': row[3],
                                  'p1_comment': row[4],
                                  'p2_score': row[5],
                                  'p2_comment': row[6],
                                  'p3_score': row[7],
                                  'p3_comment': row[8]} for row in csv_reader}

    return students_data


def send_mail(students, lucky_student, email_srv, sender):

    for student, details in students.items():
        email_body = \
            f"""Dear {details['first_name']}, Your score for the book assignment is  
            broken down below by question number.
             1. {details['p1_score']}%: {details['p1_comment']}
             2. {details['p2_score']}%: {details['p2_comment']}
             3. {details['p3_score']}%: {details['p3_comment']}
             {'You’ve been randomly chosen to present a summary ' 
              'of the book in the next class. Looking forward to it!' if student == lucky_student else ''}
            """
        email_srv.sendmail(sender, student, "Book Assignment Scores")


def main():

    # smtp server connection details
    username = input('Enter smtp username: ')
    password = input('Enter smtp password: ')
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    inspect_file('exam.csv')

    # read in student data
    students_data = save_students_data('exam.csv')

    # pick a student at random
    chosen_student_email = random.choice(list(students_data.keys()))

    pprint(chosen_student_email)

    # establish connection to the smtp server
    smtp_server.login(username, password)

    # send scores emails to students
    send_mail(students_data, chosen_student_email, smtp_server, username)

    # quit the smtp server
    smtp_server.quit()


if __name__ == '__main__':
    main()
