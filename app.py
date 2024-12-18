import streamlit as st
import pandas as pd
import altair as alt
from streamlit.logger import get_logger
import base64

LOGGER = get_logger(__name__)

def get_base64_of_bin_file(bin_file):
    """
    Read binary file and return base64 encoded string
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    """
    Set background image for Streamlit app
    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main {{
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def run():
    # Page configuration
    st.set_page_config(
        page_title="Process Scheduling Simulator",
        page_icon="🔄",
        initial_sidebar_state="collapsed",
        layout="wide",
        menu_items={
            'About': "Project by : Hussain Ahmad, Mustafa Shah, Saud Khan, Muhammad Adeel",
        }
    )

    # Try to set background image
    try:
        set_background('background_image.jpg')  # Make sure to add this file
    except FileNotFoundError:
        st.warning("Background image not found. Using default background.")

    st.markdown("""
<style>
/* Main container styling */
.main {
    background-color: rgba(248, 249, 250, 0.9);
    backdrop-filter: blur(5px);
}

/* Header styling */
.title-container {
    background-color: rgba(31, 41, 55, 0.9);
    padding: 1rem 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

/* Rest of the existing CSS remains the same... */
</style>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div class="title-container">
            <h1 style="margin: 0; font-size: 3rem; color: #ffffff;">Process Scheduling Simulator</h1>
            <p style="margin: 0; color: #9ca3af; font-size: 1.25rem;">A visual tool for understanding CPU scheduling algorithms</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)




    # Create two columns for the main layout
    left_col, right_col = st.columns([2, 1])

    with right_col:
        with st.expander("📘 About This Project", expanded=False):
            st.markdown("""
            ### Team Members
            - **Hussain Ahmad** - 2022220
            - **Mustafa Shah** - 2022407
            - **Saud Khan** - 2022533
            - **Muhammad Adeel** - 2022331
            
            ### Purpose
            This simulator helps visualize and understand different CPU scheduling algorithms through interactive simulation and visualization.
            """)

    with left_col:
        # Algorithm Selection
        st.markdown("### 🎯 Select Algorithm")
        scheduler_type = st.selectbox(
            'Choose a scheduling algorithm',
            ('FCFS (First Come First Serve)', 'SJF (Shortest Job First)', 
             'SRTF (Shortest Remaining Time First)', 'RR (Round Robin)',
             'Priority (Non-Preemptive)')
        )

        # Algorithm description card
        algorithm_descriptions = {
            'FCFS (First Come First Serve)': {
                'desc': "Processes are executed strictly in the order they arrive.",
                'pros': "Simple and fair for basic scheduling needs.",
                'cons': "Can lead to longer average waiting times."
            },
            'SJF (Shortest Job First)': {
                'desc': "Executes the process with the shortest burst time first.",
                'pros': "Optimal average waiting time for non-preemptive scheduling.",
                'cons': "May lead to starvation of longer processes."
            },
            'SRTF (Shortest Remaining Time First)': {
                'desc': "Preemptively schedules processes based on remaining time.",
                'pros': "Optimal average waiting time for preemptive scheduling.",
                'cons': "High overhead due to frequent context switching."
            },
            'RR (Round Robin)': {
                'desc': "Processes are executed in a circular manner with fixed time quantum.",
                'pros': "Fair allocation of CPU time to all processes.",
                'cons': "Performance depends heavily on quantum size."
            },
            'Priority (Non-Preemptive)': {
                'desc': "Executes processes based on priority values.",
                'pros': "Good for systems with clear process importance levels.",
                'cons': "Can lead to priority inversion and starvation."
            }
        }

        algo_info = algorithm_descriptions[scheduler_type]
        st.markdown(f"""
            <div class="algorithm-description">
                <p><strong>Description:</strong> {algo_info['desc']}</p>
                <p><strong>➕ Advantages:</strong> {algo_info['pros']}</p>
                <p><strong>➖ Disadvantages:</strong> {algo_info['cons']}</p>
            </div>
        """, unsafe_allow_html=True)

    # Process Input Section
    with left_col:
        st.markdown("### 📝 Process Entry")
        
        # Initialize session state
        if 'processes' not in st.session_state:
            st.session_state.processes = []

        # Process input form
        with st.form(key="add_process_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                arrival_time = st.number_input("Arrival Time", min_value=0, step=1)
            with col2:
                burst_time = st.number_input("Burst Time", min_value=1, step=1)
            with col3:
                if scheduler_type == "Priority (Non-Preemptive)":
                    priority = st.number_input("Priority", min_value=1, step=1)
                elif scheduler_type == "RR (Round Robin)":
                    quantum_time = st.number_input("Quantum Time", min_value=1, step=1, value=2)
                    st.session_state.quantum_time = quantum_time

            submit_process = st.form_submit_button("Add Process")
            
            if submit_process:
                process_num = len(st.session_state.processes) + 1
                process = {
                    'Process': f'P{process_num}',
                    'Arrival Time': arrival_time,
                    'Burst Time': burst_time
                }
                if scheduler_type == "Priority (Non-Preemptive)":
                    process['Priority'] = priority
                st.session_state.processes.append(process)

    # Display added processes and controls
    if st.session_state.processes:
        with right_col:
            st.markdown("### 📊 Added Processes")
            process_df = pd.DataFrame(st.session_state.processes)
            st.dataframe(process_df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear All", type="secondary"):
                    st.session_state.processes = []
                    st.experimental_rerun()
            with col2:
                calculate = st.button("Calculate", type="primary")

        # Calculate and display results
        if calculate and len(st.session_state.processes) > 0:
            try:
                # Convert data for algorithms
                arrival_times = [p['Arrival Time'] for p in st.session_state.processes]
                burst_times = [p['Burst Time'] for p in st.session_state.processes]
                labels = [p['Process'] for p in st.session_state.processes]
                data = list(zip(labels, arrival_times, burst_times))

                # Run selected algorithm
                if scheduler_type == "FCFS (First Come First Serve)":
                    start_times, completion_times, wait_times, turnaround_times = shinfcfs(data)
                elif scheduler_type == "SJF (Shortest Job First)":
                    start_times, completion_times, wait_times, turnaround_times = sjf(arrival_times, burst_times)
                elif scheduler_type == "SRTF (Shortest Remaining Time First)":
                    start_times, completion_times, wait_times, turnaround_times = srtf(arrival_times, burst_times)
                elif scheduler_type == "RR (Round Robin)":
                    start_times, completion_times, wait_times, turnaround_times = rr(data, st.session_state.quantum_time)
                elif scheduler_type == "Priority (Non-Preemptive)":
                    priority_list = [p.get('Priority', 0) for p in st.session_state.processes]
                    data, start_times, completion_times, wait_times, turnaround_times = priority(arrival_times, burst_times, priority_list)

                # Results Section
                st.markdown("### 📊 Results")
                
                # Gantt Chart
                plot_gantt_chart(scheduler_type, start_times, data)
                
                # Metrics
                col1, col2 = st.columns(2)
                avg_tat = float(sum(turnaround_times))/len(turnaround_times)
                avg_wt = float(sum(wait_times))/len(wait_times)
                
                with col1:
                    st.markdown("""
                        <div class="metric-card">
                            <h4 style="margin:0;color:#4b5563;">Average Turn Around Time</h4>
                            <p style="margin:0;font-size:1.5rem;color:#3b82f6;">{:.2f} units</p>
                        </div>
                    """.format(avg_tat), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                        <div class="metric-card">
                            <h4 style="margin:0;color:#4b5563;">Average Waiting Time</h4>
                            <p style="margin:0;font-size:1.5rem;color:#3b82f6;">{:.2f} units</p>
                        </div>
                    """.format(avg_wt), unsafe_allow_html=True)
                
                # Detailed Results Table
                st.markdown("### 📋 Detailed Process Timing")
                create_table(start_times, completion_times, wait_times, turnaround_times, data)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        elif calculate:
            st.warning("Please add at least one process before calculating.")

    # Keep the original algorithm functions unchanged
def shinfcfs(data):
    data.sort(key=lambda x: x[1])
    start_times = []
    completion_times = []
    wait_times = []
    turnaround_times = []
    last_completion_time = 0

    for i in range(len(data)):
        process_name, arrival_time, burst_time = data[i]
        if last_completion_time < arrival_time:
            start_time = arrival_time
        else:
            start_time = last_completion_time
        start_times.append(start_time)
        completion_time = start_time + burst_time
        completion_times.append(completion_time)
        last_completion_time = completion_time
        turnaround_time = completion_time - arrival_time
        turnaround_times.append(turnaround_time)
        wait_time = start_time - arrival_time
        wait_times.append(wait_time)

    return start_times, completion_times, wait_times, turnaround_times

def sjf(arrival_times, burst_times):
    n = len(arrival_times)
    completion_times = [0] * n
    wait_times = [0] * n
    turnaround_times = [0] * n
    start_times = [0] * n
    remaining_burst_times = burst_times[:]
    is_completed = [False] * n
    current_time = 0
    completed = 0

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if arrival_times[i] <= current_time and not is_completed[i] and remaining_burst_times[i] < min_burst:
                min_burst = remaining_burst_times[i]
                idx = i
        if idx != -1:
            start_times[idx] = current_time
            completion_times[idx] = current_time + burst_times[idx]
            wait_times[idx] = current_time - arrival_times[idx]
            turnaround_times[idx] = completion_times[idx] - arrival_times[idx]
            is_completed[idx] = True
            current_time += burst_times[idx]
            completed += 1
        else:
            current_time += 1

    return start_times, completion_times, wait_times, turnaround_times

def srtf(arrival_times, burst_times):
    n = len(arrival_times)
    completion_times = [0] * n
    wait_times = [0] * n
    turnaround_times = [0] * n
    start_times = [-1] * n
    remaining_burst_times = burst_times[:]
    is_completed = [False] * n
    current_time = 0
    completed = 0
    last_idx = -1

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if arrival_times[i] <= current_time and not is_completed[i] and remaining_burst_times[i] < min_burst:
                min_burst = remaining_burst_times[i]
                idx = i
        if idx != -1:
            if last_idx != idx and start_times[idx] == -1:
                start_times[idx] = current_time
            elif last_idx != idx:
                start_times[idx] = current_time
            remaining_burst_times[idx] -= 1
            if remaining_burst_times[idx] == 0:
                completion_times[idx] = current_time + 1
                wait_times[idx] = completion_times[idx] - arrival_times[idx] - burst_times[idx]
                turnaround_times[idx] = completion_times[idx] - arrival_times[idx]
                is_completed[idx] = True
                completed += 1
            last_idx = idx
        current_time += 1

    for i in range(n):
        if start_times[i] == -1:
            start_times[i] = arrival_times[i]

    return start_times, completion_times, wait_times, turnaround_times

def rr(data, quantum):
    if quantum <=0:
        st.error("Time cannot be negative or zero", icon="💅")
    data.sort(key=lambda x: x[1])
    n = len(data)
    remaining_burst_times = [x[2] for x in data]  # Initial burst times
    arrival_times = [x[1] for x in data]
    start_times = [-1] * n  # To record the first time a process is picked up
    completion_times = [0] * n
    t = 0
    queue = []
    process_index = 0

    while True:
        while process_index < n and arrival_times[process_index] <= t:
            if process_index not in queue:
                queue.append(process_index)
            process_index += 1

        if not queue:
            if process_index < n:
                t = arrival_times[process_index]
            else:
                break
        if queue:
            current_process = queue.pop(0)
            if start_times[current_process] == -1:
                start_times[current_process] = t
            
            service_time = min(quantum, remaining_burst_times[current_process])
            remaining_burst_times[current_process] -= service_time
            t += service_time

            if remaining_burst_times[current_process] == 0:
                completion_times[current_process] = t
            else:
                while process_index < n and arrival_times[process_index] <= t:
                    if process_index not in queue:
                        queue.append(process_index)
                    process_index += 1
                queue.append(current_process)

    wait_times = [0] * n
    turnaround_times = [0] * n
    for i in range(n):
        turnaround_times[i] = completion_times[i] - arrival_times[i]
        wait_times[i] = turnaround_times[i] - data[i][2]

    return start_times, completion_times, wait_times, turnaround_times

def priority(arrival_time, burst_time, p):
    p_id = [i + 1 for i in range(len(arrival_time))]
    process = {p_id[i]: [arrival_time[i], burst_time[i], p[i]] for i in range(len(arrival_time))}
    process = dict(sorted(process.items(), key=lambda item: item[1][2], reverse=True))
    start = 0
    gantt = {}
    for i in range(len(process)):
        for j in process:
            if process[j][0] <= start and j not in gantt:
                gantt[j] = [start,start+process[j][1]]
                start = start+process[j][1]
                break
    start_times = [gantt[i][0] for i in gantt]
    completion_times = [gantt[i][1] for i in gantt]
    arrival_times = [process[i][0] for i in process]
    burst_times = [process[i][1] for i in process]
    p_id = [i for i in process]
    turnaround_times = [completion_times[i] - arrival_times[i] for i in range(len(process))]
    wait_times = [turnaround_times[i] - burst_times[i] for i in range(len(process))]
    data = list(zip(p_id, arrival_times, burst_times))
    return data,start_times, completion_times, wait_times, turnaround_times

def plot_gantt_chart(scheduler_type, start_times, data):
    burst_times = [x[2] for x in data]
    labels = [x[0] for x in data]
    df = pd.DataFrame({
        'Task': labels,
        'Start': start_times,
        'Finish': [start + burst for start, burst in zip(start_times, burst_times)],
        'Duration': burst_times
    })

    # Create a chart
    chart = alt.Chart(df).mark_bar().encode(
        x='Start:Q',
        x2='Finish:Q',
        y=alt.Y('Task:N', sort=list(df['Task']), title='Process ID'),
        tooltip=['Task', 'Start', 'Finish', 'Duration']
    ).properties(
        title=f"Gantt Chart for {scheduler_type}"
    )

    st.altair_chart(chart, use_container_width=True)

def create_table(start_times, completion_times, wait_times, turnaround_times, data):
    labels = [x[0] for x in data]
    arrival_times_list = [x[1] for x in data]
    burst_times_list = [x[2] for x in data]
    table_df = pd.DataFrame({
        "Process Name" : labels,
        "Arrival Times" : arrival_times_list,
        "I/O Time" : burst_times_list,
        "Start" : start_times,
        "Finish Time" : completion_times,
        "Turn Around Time" : turnaround_times,
        "Wait Time" : wait_times,
    })
    st.dataframe(table_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    run()
