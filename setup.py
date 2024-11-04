from setuptools import setup, find_packages

setup(
    name="scored_miniproject",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pillow',
        'pydub',
        'opencv-python',
        'requests',
        'bs4',
        'groq',
        'ffmpeg-python',
        'google-generativeai',
        'transformers',
        'chromadb==0.4.18',
        'sentence_transformers',
        'zmq',
        'streamlit',
        'matplotlib',
        'pandas',
        'plotly',
        'torch',
        'fastapi'
    ]
)
