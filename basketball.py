import streamlit as st
import time
import sqlite3

# Database setup
conn = sqlite3.connect('basketball_stats.db')
c = conn.cursor()

# Create tables if not exists
c.execute('''CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS stats (player_id INTEGER, free_throw_makes INTEGER, free_throw_misses INTEGER,
                                               two_point_makes INTEGER, two_point_misses INTEGER,
                                               three_point_makes INTEGER, three_point_misses INTEGER,
                                               rebounds INTEGER, assists INTEGER, steals INTEGER, 
                                               FOREIGN KEY (player_id) REFERENCES players(id))''')
conn.commit()

# Sidebar: Add/Remove players
st.sidebar.header("Manage Players")
player_name = st.sidebar.text_input("Player Name")
if st.sidebar.button("Add Player"):
    c.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
    conn.commit()
    st.sidebar.success(f"Added {player_name}")

players = c.execute("SELECT id, name FROM players").fetchall()

# Main Page: Game Tracker
st.title("Basketball Game Tracker")

# Timer functionality
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

if st.button("Start Game"):
    st.session_state['start_time'] = time.time()

if st.session_state['start_time']:
    elapsed_time = int(time.time() - st.session_state['start_time'])
    st.header(f"Game Time: {elapsed_time // 60}:{elapsed_time % 60:02}")

# Stat Tracking
for player in players:
    player_id, name = player
    st.subheader(name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"Free Throw Make ({name})"):
            # Update stats in DB
            c.execute("UPDATE stats SET free_throw_makes = free_throw_makes + 1 WHERE player_id = ?", (player_id,))
            conn.commit()

    # Add more buttons and stat updates for other metrics...

conn.close()
