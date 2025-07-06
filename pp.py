import os
import tkinter.font as font
from tkinter import *
from tkinter import filedialog
from pyresparser import ResumeParser
from sklearn import datasets, linear_model
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

class train_model:
    
    def train(self):
        data = pd.read_csv('/home/sadiq/Desktop/rrpproject/training_dataset.csv')
        array = data.values
        for i in range(len(array)):
            if array[i][0] == "Male":
                array[i][0] = 1
            else:
                array[i][0] = 0

        df = pd.DataFrame(array)
        maindf = df[[0, 1, 2, 3, 4, 5, 6]]
        mainarray = maindf.values
        temp = df[7]
        train_y = temp.values
        
        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.mul_lr.fit(mainarray, train_y)
    
    def test(self, test_data):
        try:
            test_predict = list(map(int, test_data))
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred
        except:
            print("All Factors For Finding Personality Not Entered!")

def check_type(data):
    if isinstance(data, str):
        return str(data).title()
    if isinstance(data, (list, tuple)):
        return ", ".join(map(str, data))
    return str(data)

def OpenFile(b4):
    global loc
    name = filedialog.askopenfilename(initialdir="/home/sadiq/Desktop/rrpproject/",
                                      filetypes=(("Document", "*.docx*"), ("PDF", "*.pdf*"), ('All files', '*')),
                                      title="Choose a file."
                                      )
    try:
        filename = os.path.basename(name)
        if len(filename) > 15:
            filename = filename[:10] + "..." + filename[-5:]
        loc = name
    except:
        filename = name
        loc = name
    b4.config(text=filename)

def prediction_result(top, aplcnt_name, cv_path, personality_values):
    top.withdraw()  # Hide the main application window

    # Prepare applicant data
    applicant_data = {"Candidate Name": aplcnt_name.get(), "CV Location": cv_path}

    age = personality_values[1]  # Assuming age is at index 1 in personality_values

    print("\n############# Candidate Entered Data #############\n")
    print(applicant_data, personality_values)

    # Predict personality based on model
    personality = model.test(personality_values)
    print("\n############# Predicted Personality #############\n")
    print(personality)

    # Extract data from resume
    try:
        data = ResumeParser(cv_path).get_extracted_data()
        del data['name']  # Remove 'name' key if present
        if len(data.get('mobile_number', '')) < 10:
            del data['mobile_number']  # Remove 'mobile_number' if less than 10 characters
    except Exception as e:
        print(f"Error parsing resume: {e}")
        data = {}

    print("\n############# Resume Parsed Data #############\n")
    for key, value in data.items():
        print(f"{key}: {value}")

    # Display results in a new tkinter window
    result = Tk()
    result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
    result.configure(background='White')
    result.title("Predicted Personality")

    titleFont = font.Font(family='Arial', size=40, weight='bold')
    Label(result, text="Result - Personality Prediction", foreground='green', bg='white', font=titleFont, pady=10, anchor=CENTER).pack(fill=BOTH)

    Label(result, text=f"Name: {aplcnt_name.get()}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    Label(result, text=f"Age: {age}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    for key, value in data.items():
        Label(result, text=f"{key}: {value}", foreground='black', bg='white', anchor='w', width=60).pack(fill=BOTH)
    Label(result, text=f"Predicted Personality: {personality}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)

    quitBtn = Button(result, text="Exit", command=result.destroy).pack()

    terms_mean = """
# Openness:
    People who like to learn new things and enjoy new experiences usually score high in openness. Openness includes traits like being insightful and imaginative and having a wide variety of interests.

# Conscientiousness:
    People that have a high degree of conscientiousness are reliable and prompt. Traits include being organised, methodic, and thorough.

# Extraversion:
    Extraversion traits include being; energetic, talkative, and assertive (sometime seen as outspoken by Introverts). Extraverts get their energy and drive from others, while introverts are self-driven get their drive from within themselves.

# Agreeableness:
    As it perhaps sounds, these individuals are warm, friendly, compassionate and cooperative and traits include being kind, affectionate, and sympathetic. In contrast, people with lower levels of agreeableness may be more distant.

# Neuroticism:
    Neuroticism or Emotional Stability relates to degree of negative emotions. People that score high on neuroticism often experience emotional instability and negative emotions. Characteristics typically include being moody and tense.    
"""
    
    Label(result, text=terms_mean, foreground='green', bg='white', anchor='w', justify=LEFT).pack(fill=BOTH)

    result.mainloop()

def perdict_person():
    root.withdraw()  # Hide the main application window
    
    top = Toplevel()
    top.geometry('700x500')
    top.configure(background='black')
    top.title("Apply For A Job")

    titleFont = font.Font(family='Helvetica', size=20, weight='bold')
    Label(top, text="Personality Prediction", foreground='red', bg='black', font=titleFont, pady=10).pack()

    job_list = ('Select Job', '101-Developer at TTC', '102-Chef at Taj', '103-Professor at MIT')
    job = StringVar(top)
    job.set(job_list[0])

    Label(top, text="Applicant Name", foreground='white', bg='black').place(x=70, y=130)
    Label(top, text="Age", foreground='white', bg='black').place(x=70, y=160)
    Label(top, text="Gender", foreground='white', bg='black').place(x=70, y=190)
    Label(top, text="Upload Resume", foreground='white', bg='black').place(x=70, y=220)
    Label(top, text="Enjoy New Experience or thing (Openness)", foreground='white', bg='black').place(x=70, y=250)
    Label(top, text="How Often You Feel Negativity (Neuroticism)", foreground='white', bg='black').place(x=70, y=280)
    Label(top, text="Wishing to do one's work well and thoroughly (Conscientiousness)", foreground='white', bg='black').place(x=70, y=310)
    Label(top, text="How much would you like to work with your peers (Agreeableness)", foreground='white', bg='black').place(x=70, y=340)
    Label(top, text="How outgoing and social interaction you like (Extraversion)", foreground='white', bg='black').place(x=70, y=370)

    sName = Entry(top)
    sName.place(x=450, y=130, width=160)
    age = Entry(top)
    age.place(x=450, y=160, width=160)
    gender = IntVar()
    R1 = Radiobutton(top, text="Male", variable=gender, value=1, padx=7)
    R1.place(x=450, y=190)
    R2 = Radiobutton(top, text="Female", variable=gender, value=0, padx=3)
    R2.place(x=540, y=190)
    b4 = Button(top, text="Select File", command=lambda: OpenFile(b4))
    b4.place(x=450, y=220, width=160)
    openness = Entry(top)
    openness.insert(0, '1-10')
    openness.place(x=450, y=250, width=160)
    neuroticism = Entry(top)
    neuroticism.insert(0, '1-10')
    neuroticism.place(x=450, y=280, width=160)
    conscientiousness = Entry(top)
    conscientiousness.insert(0, '1-10')
    conscientiousness.place(x=450, y=310, width=160)
    agreeableness = Entry(top)
    agreeableness.insert(0, '1-10')
    agreeableness.place(x=450, y=340, width=160)
    extraversion = Entry(top)
    extraversion.insert(0, '1-10')
    extraversion.place(x=450, y=370, width=160)

    submitBtn = Button(top, padx=2, pady=0, text="Submit", bd=0, foreground='white', bg='red', font=(12))
    submitBtn.config(command=lambda: prediction_result(top, sName, loc, (gender.get(), age.get(), openness.get(), neuroticism.get(), conscientiousness.get(), agreeableness.get(), extraversion.get())))
    submitBtn.place(x=350, y=400, width=200)

    top.mainloop()

if __name__ == "__main__":
    model = train_model()
    model.train()

    root = Tk()
    root.geometry('700x500')
    root.configure(background='white')
    root.title("Personality Prediction System")

    titleFont = font.Font(family='Helvetica', size=25, weight='bold')
    homeBtnFont = font.Font(size=12, weight='bold')
    Label(root, text="Personality Prediction System", bg='white', font=titleFont, pady=30).pack()
    Button(root, padx=4, pady=4, width=30, text="Predict Personality", bg='black', foreground='white', bd=1, font=homeBtnFont, command=perdict_person).pack()

    root.mainloop()

