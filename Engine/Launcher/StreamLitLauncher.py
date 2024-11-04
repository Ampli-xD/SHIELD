import os
import shutil
import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from Engine.Launcher.LauncherMain import main

# Set the page config to dark mode
st.set_page_config(page_title="Interactive Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark mode and modern aesthetics
st.markdown("""
    <style>
    .css-1emrehy.edgvbvh3 {
        background-color: #0e1117;
        color: #f0f0f0;
    }
    .stButton > button {
        background-color: #1e1e2f;
        color: #f0f0f0;
        border: None;
    }
    .folder-upload {
        border: 2px dashed #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "analysis_results_fixed" not in st.session_state:
    st.session_state.analysis_results_fixed = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "folder_path" not in st.session_state:
    st.session_state.folder_path = None


# Function to simulate loading
def loading_indicator():
    with st.spinner("Loading..."):
        time.sleep(2)


def process_folder(folder_path):
    """Process all files in the folder and its subdirectories."""
    processed_files = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                processed_files.append({
                    'name': file,
                    'path': file_path,
                    'relative_path': relative_path,
                    'size': os.path.getsize(file_path) / 1024  # Size in KB
                })
        return processed_files
    except Exception as e:
        st.error(f"Error processing folder: {str(e)}")
        return []


def save_uploaded_file(uploaded_file, save_dir):
    """Save an uploaded file and return its details."""
    try:
        file_path = os.path.join(save_dir, uploaded_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return {
            'name': uploaded_file.name,
            'path': file_path,
            'type': uploaded_file.type,
            'size': uploaded_file.size / 1024  # Size in KB
        }
    except Exception as e:
        st.error(f"Error saving file {uploaded_file.name}: {str(e)}")
        return None


# User Authentication (Simplified for demonstration)
user_mode = st.sidebar.selectbox("Select User Mode", ["Guest User", "Developer"])
if user_mode == "Developer":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if username == "dev" and password == "password":
        st.session_state.logged_in = True
    else:
        st.session_state.logged_in = False

if user_mode == "Guest User" or (user_mode == "Developer" and st.session_state.get('logged_in', False)):
    loading_indicator()

    # Developer-only folder processing feature
    if user_mode == "Developer" and st.session_state.get('logged_in', False):
        st.sidebar.markdown("### Developer Features")
        folder_path = st.sidebar.text_input("Enter folder path to process:")

        if folder_path and os.path.isdir(folder_path):
            if st.sidebar.button("Process Folder"):
                with st.spinner("Processing folder..."):
                    st.session_state.folder_path = folder_path
                    processed_files = process_folder(folder_path)

                    if processed_files:
                        # Save files to the TempFileStorage
                        save_dir = 'Engine/launcher/TempFileStorage/'
                        os.makedirs(save_dir, exist_ok=True)

                        # Clear existing files in TempFileStorage
                        for item in os.listdir(save_dir):
                            item_path = os.path.join(save_dir, item)
                            if os.path.isfile(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)

                        # Copy all files from the processed folder
                        for file_info in processed_files:
                            dest_path = os.path.join(save_dir, file_info['relative_path'])
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            shutil.copy2(file_info['path'], dest_path)

                        # Update session state
                        st.session_state.uploaded_files = processed_files

                        # Display processed files
                        st.sidebar.markdown("### Processed Files")
                        for file_info in processed_files:
                            st.sidebar.text(f"• {file_info['relative_path']}")

                        st.success(f"Processed {len(processed_files)} files from folder")
        else:
            if folder_path:
                st.sidebar.error("Invalid folder path")

    # Regular file uploader interface
    uploaded_files = st.file_uploader("Upload Files (Select multiple files)", type=None, accept_multiple_files=True)
    if uploaded_files:
        save_dir = 'Engine/launcher/TempFileStorage/'
        os.makedirs(save_dir, exist_ok=True)

        processed_files = []
        for uploaded_file in uploaded_files:
            file_info = save_uploaded_file(uploaded_file, save_dir)
            if file_info:
                processed_files.append(file_info)

        if processed_files:
            st.session_state.uploaded_files = processed_files

            # Show file details
            file_details = pd.DataFrame({
                'File Name': [file['name'] for file in processed_files],
                'Path': [file['path'] for file in processed_files],
                'Size (KB)': [file['size'] for file in processed_files]
            })
            st.write(file_details)

    # Analysis Section
    if st.button("Start Analysis"):
        try:
            with st.spinner("Analyzing..."):
                results = main()
                st.session_state.analysis_results_fixed = results
                st.session_state.analysis_complete = True
                st.success("Analysis completed!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.analysis_complete = False

    # Display results only if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_results_fixed:
        scores = st.session_state.analysis_results

        # Main Dashboard Layout
        left_column, center_column = st.columns([1, 3])

        with st.sidebar:
            if not st.session_state.folder_path:  # Only show if not in folder view
                st.header("Files")
                st.subheader("Uploaded Files")

                for file in st.session_state.uploaded_files:
                    if st.button(file['name'], key=f"btn_{file['name']}"):
                        st.session_state.selected_file = file
                        for result in st.session_state.analysis_results_fixed:
                            if result['filename'] == file['name']:
                                st.session_state.analysis_results = result

        with center_column:
            if st.session_state.selected_file:
                st.header("Data Visualizations")
                selected_result = st.session_state.analysis_results

                # First row of graphs (two bar plots)
                col1, col2 = st.columns(2)

                # LLM Results Bar Plot
                with col1:
                    if 'llm_results' in selected_result:
                        fig1 = go.Figure()
                        fig1.add_trace(go.Bar(
                            x=list(selected_result['llm_results'].keys()),
                            y=list(selected_result['llm_results'].values()),
                            marker_color='#1e1e2f'
                        ))
                        fig1.update_layout(title='LLM Results Comparison',
                                           xaxis_title='Category',
                                           yaxis_title='Score',
                                           margin=dict(b=20))
                        st.plotly_chart(fig1, use_container_width=True)

                # Vector Results Bar Plot
                with col2:
                    if 'vector_results' in selected_result:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(
                            x=list(selected_result['vector_results'].keys()),
                            y=list(selected_result['vector_results'].values()),
                            marker_color='#ff7f0e'
                        ))
                        fig2.update_layout(title='Vector Results Comparison',
                                           xaxis_title='Category',
                                           yaxis_title='Score',
                                           margin=dict(b=20))
                        st.plotly_chart(fig2, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Second row of graphs
                col3, col4 = st.columns(2)

                with col3:
                    if 'combined_results' in selected_result:
                        fig3 = go.Figure()
                        fig3.add_trace(go.Bar(
                            x=list(selected_result['combined_results'].keys()),
                            y=list(selected_result['combined_results'].values()),
                            marker_color='#2ca02c'
                        ))
                        fig3.update_layout(title='Combined Results',
                                           xaxis_title='Categories',
                                           yaxis_title='Score',
                                           margin=dict(b=20))
                        st.plotly_chart(fig3, use_container_width=True)

                with col4:
                    if 'combined_results' in selected_result:
                        fig4 = go.Figure()
                        fig4.add_trace(go.Pie(
                            labels=list(selected_result['combined_results'].keys()),
                            values=list(selected_result['combined_results'].values()),
                            hole=.4,
                            marker=dict(colors=['#2ca02c', '#d62728', '#9467bd'])
                        ))
                        fig4.update_layout(title='Score Distribution')
                        st.plotly_chart(fig4, use_container_width=True)

                if 'progress_bars' in selected_result:
                    st.subheader("Detailed Scores")
                    for category in selected_result['progress_bars'].keys():
                        st.markdown(f"**{category}**: {selected_result['progress_bars'][category]:.2f}%")
                        st.progress(selected_result['progress_bars'][category] / 100)

else:
    st.warning("Please log in as a Developer to access the dashboard.")
