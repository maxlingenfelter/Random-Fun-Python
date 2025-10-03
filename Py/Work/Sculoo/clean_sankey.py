import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

# Load the data
df = pd.read_csv("Py/Work/Sculoo/CheckIn.csv")
df["checkInTime"] = pd.to_datetime(df["checkInTime"])
df = df.sort_values(["studentId", "checkInTime"])

# Parse emotions
def clean_emotions(emotion_str):
    if pd.isna(emotion_str):
        return []
    # Remove braces and split by comma
    cleaned = emotion_str.strip('{}').split(',')
    return [e.strip() for e in cleaned if e.strip()]

df['emotion_list'] = df['emojis'].apply(clean_emotions)

# Define emotion categories
positive = {'Happy', 'Excited', 'Relaxed', 'Focused'}
negative = {'Worried', 'Frustrated', 'Anxious', 'Sad', 'Mad', 'Tired'}

# Simple approach: compare first and last check-in for each student
student_changes = []

for student_id in df['studentId'].unique():
    student_data = df[df['studentId'] == student_id].sort_values('checkInTime')
    
    if len(student_data) < 2:
        continue
    
    first_emotions = set(student_data.iloc[0]['emotion_list'])
    last_emotions = set(student_data.iloc[-1]['emotion_list'])
    
    # Categorize emotions
    first_neg = len(first_emotions & negative)
    first_pos = len(first_emotions & positive)
    last_neg = len(last_emotions & negative)
    last_pos = len(last_emotions & positive)
    
    # Determine overall change
    if first_neg > first_pos and last_pos > last_neg:
        student_changes.append(("Started Negative", "Ended Positive"))
    elif first_neg > 0 and last_neg == 0:
        student_changes.append(("Had Negative Emotions", "No Negative Emotions"))
    elif first_pos == 0 and last_pos > 0:
        student_changes.append(("No Positive Emotions", "Gained Positive Emotions"))
    elif first_pos > 0 and last_pos > 0:
        student_changes.append(("Already Positive", "Stayed Positive"))

# Count transitions
transition_counts = defaultdict(int)
for source, target in student_changes:
    transition_counts[(source, target)] += 1

# Create Sankey data
labels = ["Started Negative", "Had Negative Emotions", "No Positive Emotions", "Already Positive",
          "Ended Positive", "No Negative Emotions", "Gained Positive Emotions", "Stayed Positive"]

source_indices = []
target_indices = []
values = []

for (source, target), count in transition_counts.items():
    if count > 0:
        source_indices.append(labels.index(source))
        target_indices.append(labels.index(target))
        values.append(count)

# Colors: red for negative states, green for positive states
colors = ['#FF6B6B', '#FF6B6B', '#FFE66D', '#90EE90',  # sources
          '#90EE90', '#90EE90', '#90EE90', '#90EE90']   # targets

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values
    )
)])

fig.update_layout(
    title_text="Student Emotional Journey: First vs Last Check-in",
    font_size=10
)

print("Transition Summary:")
for (source, target), count in sorted(transition_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{source} → {target}: {count} students")

fig.show()
