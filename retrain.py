import sqlite3
import joblib
import pandas as pd

old_data = pd.read_csv("data/final_data.csv")
conn = sqlite3.connect("placement.db")



new_data = pd.read_sql_query(
    """
    SELECT
        IQ,
        CGPA,
        Academic_Performance,
        Internship_Experience,
        Extra_Curricular_Score,
        Communication_Skills,
        Projects_Completed,
        actual_placement AS Placement

    FROM students

    WHERE actual_placement
          IS NOT NULL
    """,
    conn
)

conn.close()



if new_data.shape[0] < 100:
    print('Gathered Data size is not sufficiently large!!')
    
    while True:
        answer = input('Do you wish to continue?[y/n]: ')

        if answer == 'n':
            print('Stopping Retraining...!!')
            exit()
        elif answer == 'y':
            break
        elif answer != 'n' or answer != 'y':
            print('Answer valid inputs from [y/n]!!')


# if your csv data has already been moved inside database then no need to use combined data, instead use only new_data.
combined = pd.concat(
    [old_data, new_data],
    ignore_index=True
)
combined.drop_duplicates(inplace=True)


X = combined.drop(columns=['Placement'])
y = combined['Placement']

model = joblib.load('placement_predictor.pkl')
model.fit(X, y)

joblib.dump(model, 'placement_predictor.pkl')