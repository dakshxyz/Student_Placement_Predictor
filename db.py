import sqlite3
import pandas as pd
import joblib

conn = sqlite3.connect("placement.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    IQ INTEGER,
    CGPA REAL,
    Academic_Performance INTEGER,
    Internship_Experience INTEGER,
    Extra_Curricular_Score INTEGER,
    Communication_Skills INTEGER,
    Projects_Completed INTEGER,
    
    predicted_placement INTEGER,
    actual_placement INTEGER DEFAULT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()



def insert_student(row):
    row = tuple(row)
    
    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO students(
        IQ,
        CGPA,
        Academic_Performance,
        Internship_Experience,
        Extra_Curricular_Score,
        Communication_Skills,
        Projects_Completed,

        predicted_placement)
        
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", row)
    
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return student_id
        
    
    
def get_all_students():
    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()
    
    

def save_prediction(
    iq,
    cgpa,
    academic,
    internship,
    extra,
    communication,
    projects,
    prediction
):
    student_id = insert_student((iq, cgpa, academic, internship, extra, communication, projects, prediction))
    return student_id



def update_actual_placement(
    student_id,
    actual_placement
):

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET actual_placement = ?
        WHERE id = ?
        """,
        (actual_placement, student_id)
    )

    conn.commit()
    conn.close()
    
    
    
def get_total_predictions():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



def get_predicted_placed():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
        WHERE predicted_placement = 1
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



def get_predicted_not_placed():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
        WHERE predicted_placement = 0
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



def get_feedback_received():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
        WHERE actual_placement IS NOT NULL
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



def get_pending_feedback():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
        WHERE actual_placement IS NULL
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result



def get_live_accuracy():

    conn = sqlite3.connect("placement.db")

    query = """
    SELECT
        predicted_placement,
        actual_placement
    FROM students
    WHERE actual_placement IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    if len(df) == 0:
        return None

    return (
        (df["predicted_placement"]
         ==
         df["actual_placement"])
        .mean()
    )
    

def get_recent_predictions():

    conn = sqlite3.connect("placement.db")

    query = """
    SELECT *
    FROM students
    ORDER BY id DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df



def deleteTable():
    while True:
        answer = input('\nThis action is not reversible!\nDo you wish to continue?[y/n]: ')
        if answer == 'n': return
        elif answer == 'y':
            print('Deleting Table....!')
            break
        else: 
            print('Enter valid answer')
    
    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE students
        """)

    conn.commit()
    conn.close()
    print('Table Deleted!')
    
    
    
    
def move_csv_to_database():
    df = pd.read_csv('data/final_data.csv')
        
    model = joblib.load('placement_predictor.pkl')
    pred = model.predict(df.drop(columns=['Placement']))

    df['predicted_placement'] = pred

    df['Placement'], df['predicted_placement'] = df['predicted_placement'], df['Placement']
    df = df.rename(columns={'Placement': 'actual_placement'})

    conn = sqlite3.connect("placement.db")
    df.to_sql("students", conn, if_exists="append", index=False)
    conn.close()
    
    