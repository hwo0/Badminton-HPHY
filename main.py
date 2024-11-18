import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import sqlite3

# def truncate_players_table():
#     conn = sqlite3.connect('hphy_badminton.db')
#     c = conn.cursor()
#     c.execute('DROP Table players')
#     conn.commit()
#     conn.close()
#     print("Table 'players' truncated successfully.")

# truncate_players_table()

# Function to ensure the required columns are present and correctly named in the DataFrame
def ensure_columns(df, column_mappings):
    for orig_col, new_col in column_mappings.items():
        if orig_col in df.columns:
            df = df.rename(columns={orig_col: new_col})
        elif new_col not in df.columns:
            df[ new_col ] = None
    return df

# Initialise the SQLite database
def init_db():
    conn = sqlite3.connect('hphy_badminton.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_names TEXT NOT NULL,
            gender TEXT,
            skill_level TEXT,
            rating INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS scheduler (
            name TEXT NOT NULL,
            time_0700 TEXT,
            time_0715 TEXT,
            time_0730 TEXT,
            time_0745 TEXT,
            time_0800 TEXT,
            time_0815 TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Load player data from SQLite
def load_player_data():
    conn = sqlite3.connect('hphy_badminton.db')
    df = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()
    if df.empty:
        df = pd.DataFrame([   
            {"Player Names": "Pan", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Anita", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Sam", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Vito", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Jackson", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Alan", "Gender": "M", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Yolanda", "Gender": "F", "Skill Level": "Beginner", "Rating": 3},
            {"Player Names": "Wayne", "Gender": "M", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Jane", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Aki", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Helen", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Henry", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "M", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Keri", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Frank Z", "Gender": "M", "Skill Level": "Advanced", "Rating": 1},
            {"Player Names": "Ray c", "Gender": "M", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Qian", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Edward", "Gender": "M", "Skill Level": "Beginner", "Rating": 3},
            {"Player Names": "Xiaoyi", "Gender": "F", "Skill Level": "Beginner", "Rating": 3},
            {"Player Names": "Phil", "Gender": "M", "Skill Level": "Beginner", "Rating": 3},
            {"Player Names": "Echo", "Gender": "F", "Skill Level": "Beginner", "Rating": 3},
            {"Player Names": "Isadora", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Vincy", "Gender": "F", "Skill Level": "Intermediate", "Rating": 2},
            {"Player Names": "Karen", "Gender": "F", "Skill Level": "Beginner", "Rating": 3}
         ])
    return df

# Save player data to SQLite
def save_player_data(df):
    conn = sqlite3.connect('hphy_badminton.db')
    df = df.rename(columns={"Player Names": "player_names", "Gender": "gender", "Skill Level": "skill_level", "Rating": "rating"})
    df.to_sql('players', conn, if_exists='replace', index=False)
    conn.close()

# Load scheduler data from SQLite
def load_scheduler_data():
    conn = sqlite3.connect('hphy_badminton.db')
    df = pd.read_sql_query("SELECT * FROM scheduler", conn)
    conn.close()
    if df.empty:
        df = pd.DataFrame(default_data)
    return df

# Save scheduler data to SQLite
def save_scheduler_data(df):
    conn = sqlite3.connect('hphy_badminton.db')
    df.to_sql('scheduler', conn, if_exists='replace', index=False)
    conn.close()

# Initialise the database
init_db()

##################--STREAMLIT FRONTEND STARTS HERE--#######################

st.title("🌞 Hi! This is an app built for HPHY Badminton Games 🏸")
st.subheader(" Dedicated to Pan, Anita & Samantha with 💕 ")
st.subheader("*** ๑>◡<๑ *** ๑>◡<๑ *** ๑>◡<๑ *** ")

# Instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Edit 'Player Names' in the top table above. (Other columns can be ignored)
2. Click 'Save Player Data' button to save player names & retain your latest edits for the next session
2. Click 'Update Data' button to transfer player names onto Scheduler
3. Drag and drop court numbers to swap values inside the Scheduler

Note: Edits in Scheduler is not retained and resets to default on each session.

(Development Version 1.0 - 18/11/2024)
""")

st.header("Input Player Data Here")

# Default data for Scheduler
default_data = {
    'Name': [  'Pan', 'Anita', 'Sam', 'Pan', 'Vito', 'M', 'Benny', 'Wayne', 'Kai', 'Derek Lam',
              'Alan', 'Sandor', 'Binnie', 'Helen', 'Tina', 'Frank', 'Jane', 'Phil', 'Frank Li', 
              'Henry', 'Isadora', 'Ray', 'Qian', 'Vincy'  ],
    '7:00': [  '/', '/', '5', '5', '5', '5', '7', '/', '/', '7', '7', '7', '/', '/', '6', '6', 
              '6', '/', '6', '4', '/', '4', '4', '4'  ],
    '7:15': [  '5', '5', '/', '/', '5', '5', '7', '7', '7', '/', '/', '7', '6', '6', '6', '6', 
              '4', '4', '/', '/', '/', '/', '4', '4'  ],
    '7:30': [  '4', '4', '4', '4', '/', '/', '/', '7', '7', '5', '5', '/', '7', '7', '/', '/', 
              '/', '6', '6', '6', '5', '5', '6', '/'  ],
    '7:45': [  '/', '/', '6', '7', '7', '4', '4', '/', '/', '6', '6', '6', '/', '/', '7', '7', 
              '4', '/', '5', '5', '/', '4', '5', '5'  ],
    '8:00': [  '5', '5', '/', '/', '7', '7', '6', '4', '4', '/', '/', '6', '5', '5', '7', '7', 
              '4', '6', '/', '/', '4', '/', '/', '6'  ],
    '8:15' :[  '4', '4', '4', '6', '/', '/', '/', '4', '6', '7', '7', '/', '6', '6', '/', '/', 
              '/', '5', '5', '7', '5', '5', '7', '/'  ]
}

# Check if session state and columns are already initialised
if 'players_df' not in st.session_state:
    st.session_state.players_df = load_player_data()

# Ensure the necessary columns exist before proceeding
needed_columns = {
    "player_names": "Player Names",
    "gender": "Gender",
    "skill_level": "Skill Level",
    "rating": "Rating"
}
st.session_state.players_df = ensure_columns(st.session_state.players_df, needed_columns)

# Convert 'Skill Level' column to a categorical type with specific categories
skill_levels = [ "Beginner", "Intermediate", "Advanced" ]
st.session_state.players_df[ "Skill Level" ] = pd.Categorical(
    st.session_state.players_df[ "Skill Level" ],
    categories=skill_levels,
    ordered=True
)

# Calculate the height of the data editor to display all rows
row_height = 36  # Adjust this value based on your styling and preferences
num_rows = len(st.session_state.players_df)
editor_height = row_height * (num_rows + 1)  # +1 for the header row

# Display and allow editing of the dataframe
st.session_state.players_df = st.data_editor(
    st.session_state.players_df, 
    height=editor_height, 
    width=800, 
    num_rows="dynamic",
    column_config={
        "Skill Level": st.column_config.SelectboxColumn(options=skill_levels)
    }
)

# Save player data if 'Save Player Data' button is clicked
if st.button('Save Player Data'):
    save_player_data(st.session_state.players_df)
    st.success("Player data saved successfully!")

# Initialise scheduler data
if 'scheduler_df' not in st.session_state:
    st.session_state.scheduler_df = pd.DataFrame(default_data)

df = st.session_state.scheduler_df

# Function to update the 'scheduler_df' DataFrame with the edited 'players_df' DataFrame
def update_data():
    new_names = st.session_state.players_df[ "Player Names" ].tolist()
    df[ "Name" ] = new_names[ :len(df) ]  # Update only up to the length of the existing 'df'
    st.session_state.scheduler_df = df
    st.session_state.updated_data_html = df.to_html(classes='dataframe', index=False, escape=False)

# Add button to update data
if st.button('Update Data'):
    update_data()

st.header("Sunday Games Scheduler")

# Display updated data if the button has been clicked
if 'updated_data_html' in st.session_state:
    html_table = st.session_state.updated_data_html
else:
    html_table = df.to_html(classes='dataframe', index=False, escape=False)

# Estimate height for DataFrame display
row_height = 35  # Approximate height of each row in pixels
header_height = 40  # Approximate height of the header in pixels
total_height = header_height + (len(df) * row_height) + 50  # Add some padding

# JavaScript and HTML for drag-and-drop functionality with improved styling
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Drag and Drop Table Cells</title>
<style>
  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'DejaVu Sans', sans-serif;
    font-size: 14px;
  }}
  th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    text-align: centre;
  }}
  th {{
    padding-top: 12px;
    padding-bottom: 12px;
    background-colour: #4CAF50;
    colour: white;
  }}
  tr:nth-child(even) {{background-colour: #f2f2f2;}}
  tr:hover {{background-colour: #ddd;}}
  .dragging {{
    background-colour: #e0e0e0;
  }}
</style>
</head>
<body>
{html_table}

<script>
document.addEventListener('DOMContentLoaded', () => {{
  let draggingCell;

  document.querySelectorAll('td').forEach(cell => {{
    cell.setAttribute('draggable', 'true');

    cell.addEventListener('dragstart', (event) => {{
      draggingCell = event.target;
      event.target.classList.add('dragging');
      event.dataTransfer.effectAllowed = 'move';
    }});

    cell.addEventListener('dragend', (event) => {{
      event.target.classList.remove('dragging');
    }});

    cell.addEventListener('dragover', (event) => {{
      event.preventDefault();
      event.dataTransfer.dropEffect = 'move';
    }});

    cell.addEventListener('drop', (event) => {{
      event.preventDefault();
      if (draggingCell !== event.target) {{
        let tempContent = event.target.innerHTML;
        event.target.innerHTML = draggingCell.innerHTML;
        draggingCell.innerHTML = tempContent;
      }}
    }});
  }});
}});
</script>
</body>
</html>
"""
# Embed the HTML and JavaScript in the Streamlit app
st.components.v1.html(html_code, height=total_height, scrolling=False)

# Save scheduler data if 'Save Schedule' button is clicked
# if st.button('Save Schedule'):
#     # Save the updated scheduler_df into the database
#     if 'scheduler_df' in st.session_state:
#         save_scheduler_data(st.session_state.scheduler_df)
#         st.success("Schedule saved successfully!")
