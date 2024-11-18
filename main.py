
import streamlit as st
from streamlit.components.v1 import html
import pandas as pd


##################--STREAMLIT FRONTEND STARTS HERE--#######################

st.title("🌞 Hi! This is an app built for HPHY Badminton Games 🏸")
st.subheader(" Dedicated to Pan, Anita & Samantha with 💕 ")
st.subheader("*** ๑>◡<๑ *** ๑>◡<๑ *** ๑>◡<๑ *** ")

# Instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Edit 'Player Names' in top table above. (Other columns can be ignored)
2. Click 'Update Data' button to transfer player names onto Scheduler
3. Drag and drop court numbers to swap values inside Scheduler
4. The app will retain your latest edits for the next session.

(Development Version 1.0 - 18/11/2024)
""")

##############################################################################

st.header("Input Player Data Here")

# Initialise session state
if 'players_df' not in st.session_state:
    st.session_state.players_df = pd.DataFrame([ 
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
    
# Convert 'Skill Level' column to a categorical type with specific categories
skill_levels = [ "Beginner", "Intermediate", "Advanced" ]
st.session_state.players_df[ "Skill Level" ] = pd.Categorical(
    st.session_state.players_df[ "Skill Level" ], categories=skill_levels, ordered=True
)

# Calculate the height of the data editor to display all rows
row_height = 36  # Adjust this value based on your styling and preferences
num_rows = len(st.session_state.players_df)
editor_height = row_height * (num_rows + 1)  # +1 for the header row

# Display and allow editing of the dataframe
st.session_state.players_df = st.data_editor(
                              st.session_state.players_df, 
                              height=editor_height, 
                              width = 800, 
                              num_rows="dynamic",
                              column_config= {
                                  "Skill Level": st.column_config.SelectboxColumn(options = skill_levels)
                              }
                              )

# st.write(st.session_state.players_df)
###################################

# Sample DataFrame
data = {
    'Name': [  'Pan', 'Anita', 'Sam', 'Pan', 'Vito', 'M', 'Benny', 'Wayne', 'Kai', 'Derek Lam', 'Alan', 'Sandor', 'Binnie',
             'Helen', 'Tina', 'Frank', 'Jane', 'Phil', 'Frank Li', 'Henry', 'Isadora', 'Ray', 'Qian', 'Vincy'  ],
    '7:00': [  '/', '/', 5, 5, 5, 5, 7, '/', '/', 7, 7, 7, '/', '/', 6, 6, 6, '/', 6, 4, '/', 4, 4, 4  ],
    '7:15': [  5, 5, '/', '/', 5, 5, 7, 7, 7, '/', '/', 7, 6, 6, 6, 6, 4, 4, '/', '/', '/', '/', 4, 4  ],
    '7:30': [  4, 4, 4, 4, '/', '/', '/', 7, 7, 5, 5, '/', 7, 7, '/', '/', '/', 6, 6, 6, 5, 5, 6, '/'  ],
    '7:45': [  '/', '/', 6, 7, 7, 4, 4, '/', '/', 6, 6, 6, '/', '/', 7, 7, 4, '/', 5, 5, '/', 4, 5, 5  ],
    '8:00': [  5, 5, '/', '/', 7, 7, 6, 4, 4, '/', '/', 6, 5, 5, 7, 7, 4, 6, '/', '/', 4, '/', '/', 6  ],
    '8:15': [  4, 4, 4, 6, '/', '/', '/', 4, 6, 7, 7, '/', 6, 6, '/', '/', '/', 5, 5, 7, 5, 5, 7, '/'  ]
}

df = pd.DataFrame(data)
####################
# Function to update the 'data' DataFrame with the edited 'players_df' DataFrame
def update_data():
    new_names = st.session_state.players_df[ 'Player Names' ].tolist()
    df[ 'Name' ] = new_names[ :len(df) ]  # Update only up to the length of the existing 'df'
    st.session_state.updated_data_html = df.to_html(classes='dataframe', index=False, escape=False)

# Add button to update data
if st.button('Update Data'):
    update_data()


st.header("Sunday Games Scheduler")

# Display updated data if button has been clicked
if 'updated_data_html' in st.session_state:
    html_table = st.session_state.updated_data_html
else:
    html_table = df.to_html(classes='dataframe', index=False, escape=False)


# # ###############
# html_table = df.to_html(classes='dataframe', index=False, escape=False)
# html_table = html_table.replace('<td>', '<td contenteditable="true">')

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
