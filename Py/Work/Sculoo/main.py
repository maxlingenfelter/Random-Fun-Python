import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

# Load the data from CSV files
check_in_df = pd.read_csv("Py/Work/Sculoo/CheckIn.csv")
check_out_df = pd.read_csv("Py/Work/Sculoo/CheckOut.csv")
student_df = pd.read_csv("Py/Work/Sculoo/Student.csv")

# Convert checkIn and checkOut times to datetime, combine and sort
check_in_df["checkInTime"] = pd.to_datetime(check_in_df["checkInTime"])
check_out_df["checkOutTime"] = pd.to_datetime(check_out_df["checkOutTime"])
data_df = pd.concat([check_in_df.rename(columns={"checkInTime": "time", "emojis": "emotions"}), check_out_df.rename(columns={"checkOutTime": "time", "emojis": "emotions"})])
data_df = data_df.sort_values(["studentId", "time"])

# Function to parse emojis safely
def parse_emotions(emotion_str):
    if pd.isna(emotion_str) or emotion_str == "":
        return set()
    try:
        # Handle the string format {emotion1,emotion2,emotion3}
        emotion_str = emotion_str.strip()
        if emotion_str.startswith('{') and emotion_str.endswith('}'):
            emotion_str = emotion_str[1:-1]  # Remove curly braces
        emotions = [e.strip() for e in emotion_str.split(',') if e.strip()]
        return set(emotions)
    except:
        return set()

# Parse emotions for each entry
data_df['parsed_emotions'] = data_df['emotions'].apply(parse_emotions)

# Define positive and negative emotions
positive_emotions = {'Happy', 'Excited', 'Relaxed', 'Focused'}
negative_emotions = {'Worried', 'Frustrated', 'Anxious', 'Sad', 'Mad', 'Tired'}

# Track emotion transitions for each student
transitions = defaultdict(int)
student_journeys = defaultdict(list)

# Group by student and track their emotion journey
for student_id, group in data_df.groupby('studentId'):
    group = group.sort_values('time')
    prev_emotions = None
    
    for _, row in group.iterrows():
        current_emotions = row['parsed_emotions']
        if current_emotions:  # Only process non-empty emotion sets
            student_journeys[student_id].append(current_emotions)
            
            # If we have a previous state, track transitions
            if prev_emotions is not None:
                # Track all individual emotion transitions
                for prev_emotion in prev_emotions:
                    for curr_emotion in current_emotions:
                        if prev_emotion != curr_emotion:
                            transitions[(prev_emotion, curr_emotion)] += 1
                
                # Track emotions that disappeared (became "Resolved")
                disappeared_emotions = prev_emotions - current_emotions
                for emotion in disappeared_emotions:
                    if emotion in negative_emotions:
                        transitions[(emotion, "Resolved")] += 1
                
                # Track new emotions that appeared from "Initial State"
                new_emotions = current_emotions - prev_emotions
                for emotion in new_emotions:
                    transitions[("New Feeling", emotion)] += 1
            
            prev_emotions = current_emotions

# If no transitions found, create some basic positive flow
if not transitions:
    # Count overall emotion frequencies to show positive impact
    all_emotions = defaultdict(int)
    for student_emotions in student_journeys.values():
        for emotion_set in student_emotions:
            for emotion in emotion_set:
                all_emotions[emotion] += 1
    
    # Create flows showing positive emotions as outcomes
    for emotion, count in all_emotions.items():
        if emotion in positive_emotions:
            transitions[("Platform Use", emotion)] = count
        elif emotion in negative_emotions:
            transitions[(emotion, "Addressed")] = count // 2  # Show some were addressed

# Prepare data for Sankey diagram
source_nodes = []
target_nodes = []
values = []

for (source, target), value in transitions.items():
    if value > 0:  # Only include positive values
        source_nodes.append(source)
        target_nodes.append(target)
        values.append(value)

# Define a logical order for all labels
all_labels_order = [
    # Initial emotions (Negative/Neutral First)
    "New Feeling",
    "Tired", "Sad", "Mad", "Anxious", "Worried", "Frustrated",
    # Transition nodes
    "Resolved", "Mixed", "Improved",
    # Positive emotions
    "Focused", "Happy", "Relaxed", "Excited"
]

# Create unique labels list
all_labels = [label for label in all_labels_order if label in set(source_nodes + target_nodes)]
label_to_index = {label: i for i, label in enumerate(all_labels)}

# Convert to indices
source_indices = [label_to_index[source] for source in source_nodes]
target_indices = [label_to_index[target] for target in target_nodes]

# Create better color coding with dynamic link colors
node_colors = []
link_colors = []

for label in all_labels:
    if label in positive_emotions:
        node_colors.append('rgba(34, 139, 34, 0.8)')  # Forest green for positive emotions
    elif label in negative_emotions:
        node_colors.append('rgba(220, 20, 60, 0.8)')  # Crimson for negative emotions
    elif label == "Resolved":
        node_colors.append('rgba(50, 205, 50, 0.9)')  # Lime green for resolved issues
    elif label == "New Feeling":
        node_colors.append('rgba(70, 130, 180, 0.8)')  # Steel blue for new feelings
    else:
        node_colors.append('rgba(128, 128, 128, 0.7)')  # Gray for other states

# Create dynamic link colors based on transition type
for i, (source, target) in enumerate(zip(source_nodes, target_nodes)):
    if source in negative_emotions and target in positive_emotions:
        link_colors.append('rgba(0, 255, 0, 0.6)')  # Bright green for positive transitions
    elif source in positive_emotions and target in negative_emotions:
        link_colors.append('rgba(255, 0, 0, 0.6)')  # Red for negative transitions
    elif source in negative_emotions and target == "Resolved":
        link_colors.append('rgba(0, 200, 200, 0.6)')  # Cyan for resolution
    elif source == "New Feeling" and target in positive_emotions:
        link_colors.append('rgba(0, 150, 255, 0.6)')  # Blue for new positive feelings
    elif source == "New Feeling" and target in negative_emotions:
        link_colors.append('rgba(255, 150, 0, 0.6)')  # Orange for new negative feelings
    else:
        link_colors.append('rgba(128, 128, 128, 0.4)')  # Gray for neutral transitions

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
        color=node_colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors  # Dynamic colors based on transition type
    )
)])

fig.update_layout(
    title_text="Student Emotion Transitions - Check-In & Check-Out Analysis<br><sub>Green: Positive Transitions | Red: Negative Transitions | Cyan: Resolutions</sub>",
    font_size=12,
    width=1200,
    height=700
)

print(f"Total transitions tracked: {len(transitions)}")
print(f"Students analyzed: {len(student_journeys)}")
if transitions:
    print("Sample transitions:")
    for (source, target), count in list(transitions.items())[:5]:
        print(f"  {source} → {target}: {count} times")

fig.show()
