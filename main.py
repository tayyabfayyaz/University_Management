import streamlit as st
import json

class Student:
    def __init__(self, name, roll_no, course, paid_fee):
        self.name = name
        self.roll_no = roll_no
        self.course = course
        self.paid_fee = paid_fee
        self.subjects = []
        self.marks = []
    
    def pay_fee(self, amount):
        self.paid_fee += amount
        st.write(f"Fee paid: {amount}")
        st.write(f"Total fee paid: {self.paid_fee}")
    
    def result(self):
        st.write(f'Subjects: {self.subjects}')
        st.write(f'Marks: {self.marks}')
    
    def student_details(self):
        st.write(f"Name: {self.name}")
        st.write(f"Roll No: {self.roll_no}")
        st.write(f"Course: {self.course}")
        st.write(f"Paid Fee: {self.paid_fee}")

class UniversitySystem:
    def __init__(self):
        self.students = {}
        self.load_students()
    
    def load_students(self):
        try:
            with open("students.json", "r") as f:
                data = json.load(f)
                for roll_no, student_data in data.items():
                    self.students[roll_no] = Student(
                        student_data["name"],
                        roll_no,
                        student_data["course"],
                        student_data["paid_fee"]
                    )
        except FileNotFoundError:
            pass

    def save_students(self):
        data = {
            roll_no: {
                "name": student.name,
                "course": student.course,
                "paid_fee": student.paid_fee
            }
            for roll_no, student in self.students.items()
        }
        with open("students.json", "w") as f:
            json.dump(data, f, indent=2)


    def admit_student(self, name, roll_no, course):
        if roll_no in self.students:
            return False, "Student's Roll number already exists."
        else:
            new_student = Student(name, roll_no, course, 0)
            self.students[roll_no] = new_student
            self.save_students()
            return True, "Student admitted successfully."
    
    def submit_fee(self, roll_no, amount):
        if roll_no in self.students:
            self.students[roll_no].pay_fee(float(amount))
            self.save_students()
            return True, "Fee submitted successfully."
        else:
            return False, "Student not found."
    
    def get_student_details(self, roll_no):
        if roll_no in self.students:
            return True, self.students[roll_no].student_details()
        else:
            return False, "Student not found."
    
    def get_student_result(self, roll_no):
        if roll_no in self.students:
            return True, self.students[roll_no].result()
        else:
            return False, "Student not found."

def main():
    st.title("University Management System")
    st.subheader("Student Admission and Fee Payment System")
    st.sidebar.title("Navigation")
    system = UniversitySystem()
    select_action = st.sidebar.selectbox("Select an option", [
        "Admit Student", 
        "Submit Fee", 
        "View Student Details", 
        "View Student Result"
    ])
    
    if select_action == "Admit Student":
        st.subheader("Admit Student")
        name = st.text_input("Enter Student Name")
        roll_no = st.text_input("Enter Roll Number")
        course = st.text_input("Enter Course")
        
        if st.button("Admit"):
            success, message = system.admit_student(name, roll_no, course)
            if success:
                st.success(message)
            else:
                st.error(message)

    elif select_action == "Submit Fee":
        st.subheader("Submit Fee")
        roll_no = st.text_input("Enter your Roll Number")
        amount = st.text_input("Enter Fee Amount")
        
        if st.button("Send amount"):
            success, message = system.submit_fee(roll_no, amount)
            if success:
                st.success(message)
            else:
                st.error(message)

    elif select_action == "View Student Details":
        st.subheader("View Student Details")
        roll_no = st.text_input('Enter Roll Number')
        if st.button("Get Details"):
            success, message = system.get_student_details(roll_no)
            if success:
                message
            else:
                st.error(message)
    
    elif select_action == "View Student Result":
        st.subheader("View Student Result")
        roll_no = st.text_input("Enter Roll Number")
        if st.button('Get Result'):
            success, message = system.get_student_result(roll_no)
            if success:
                message
            else:
                st.error(message)
    
    st.sidebar.write("Developed By Tayyab Fayyaz.")

if __name__ == "__main__":
    main()
