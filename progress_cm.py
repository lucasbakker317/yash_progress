import streamlit as st
from datetime import datetime
from datetime import date
import pandas as pd
import json
import os




# Page configuration with name and page icon
st.set_page_config(page_title="Progress CMs", page_icon="✅", layout="wide", initial_sidebar_state="auto", menu_items=None)

# Page title
st.title("Progress for Content Managers")

st.write(f'Today is {datetime.now().strftime("%d %B, %Y")}')

CHECKLIST_FILE = '/Users/lucasbakker/Documents/Projects/yash_progress/checklist.json'

def reorder_tasks():
    st.session_state['tasks'].sort(key=lambda x: x['deadline'])

# Function to delete a task
def delete_item(index):
    st.session_state['tasks'].pop(index)
    save_tasks(st.session_state['tasks'])

# Initialize session state for checklist tasks
def load_tasks():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(CHECKLIST_FILE, 'w') as file:
        json.dump(tasks, file, default=str)

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

def add_item():
    left, right = st.columns([1,1])
    item = left.text_input("Add new tasks")
    deadline = right.date_input("Task deadline", value=None)
    if st.button("Add"):
        st.session_state['tasks'].append({'task':item, 'deadline':deadline, 'checked': False})
        save_tasks(st.session_state['tasks'])




def show_checklist():

    if len(st.session_state['tasks'])!=0:
        if type(st.session_state['tasks'][-1]['deadline']) == str:
            for task in st.session_state['tasks']:
                task['deadline'] = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
    
    st.session_state['tasks'] = sorted(st.session_state['tasks'], key=lambda x: x['deadline'])
    save_tasks(st.session_state['tasks'])
    
    tasks_to_delete = []
    for index, item in enumerate(st.session_state['tasks']):

        col1, col2, col3 = st.columns([1,1,1])
        is_checked = col1.checkbox(item['task'], value=item['checked'], key=index)
        st.session_state['tasks'][index]['checked'] = is_checked

        with col2:

            if item['deadline']==None:
                st.write(f"No deadline given...")
                
            else:
                if type(item['deadline'])==str:
                    d = datetime.strptime(item['deadline'], '%Y-%m-%d').date()
                    deadline_days = (d - date.today()).days
                    
                else:
                    deadline_days = (item['deadline'] - date.today()).days
                
                if deadline_days < 0:
                    st.write(f":red[This should have been completed {abs(deadline_days)} days ago]")

                else:
                    st.write(f"{deadline_days} days left to complete")
            
        with col3:

  
            if st.button(f"❌ Delete task {index + 1}"):
                st.session_state['tasks'].pop(index)
                save_tasks(st.session_state['tasks'])
                st.rerun()
                
        




add_item()
show_checklist()




completed_tasks = sum([task['checked'] for task in st.session_state['tasks']])
nr_tasks = len(st.session_state['tasks'])

st.write("#")
st.write("#")
if nr_tasks==0:
    st.progress(0, text=f"Progress of tasks: 0%")
else:
    st.progress(completed_tasks/nr_tasks, text=f"Progress of tasks: {round(100 * completed_tasks/nr_tasks, 1)}%")
