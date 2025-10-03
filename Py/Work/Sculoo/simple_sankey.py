import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

# Load the data from CSV files
check_in_df = pd.read_csv("Py/Work/Sculoo/CheckIn.csv")

# Convert checkInTime to datetime and sort by student and time
check_in_df["checkInTime"] = pd.to_datetime(check_in_df["checkInTime"])
check_in_df = check_in_df.sort_values(["studentId", "checkInTime"])

# Function to parse emotions safely
def parse_emotions(emotion_str):
    if pd.isna(emotion_str) or emotion_str == "":
        return set()
    try:
        emotion_str = emotion_str.strip()
        if emotion_str.startswith('{') and emotion_str.endswith('}'):
            emotion_str = emotion_str[1:-1]
        emotions = [e.strip() for e in emotion_str.split(',') if e.strip()]
        return set(emotions)
    except:
        return set()

# Parse emotions for each check-in
check_in_df['parsed_emotions'] = check_in_df['emojis'].apply(parse_emotions)

# Define emotion categories
positive_emotions = {'Happy', 'Excited', 'Relaxed', 'Focused'}
negative_emotions = {'Worried', 'Frustrated', 'Anxious', 'Sad', 'Mad', 'Tired'}

# Create simplified transitions focusing on the main story
transitions = defaultdict(int)

# Analyze students' first vs later emotions to show improvement
for student_id, group in check_in_df.groupby('studentId'):
    group = group.sort_values('checkInTime')
    
    if len(group) < 2:
        continue
    
    # Get first and last emotional states
    first_emotions = group.iloc[0]['parsed_emotions']
    last_emotions = group.iloc[-1]['parsed_emotions']
    
    if not first_emotions or not last_emotions:
        continue
    
    # Count initial emotional states
    first_negative = first_emotions & negative_emotions
    first_positive = first_emotions & positive_emotions
    
    # Count final emotional states
    last_negative = last_emotions & negative_emotions
    last_positive = last_emotions & positive_emotions
    
    # Create flows from initial to final states
    if first_negative and last_positive:
        # Negative to positive transition (improvement)
        for neg in first_negative:
            for pos in last_positive:
                transitions[(neg, pos)] += 1
    
    if first_negative and not last_negative:
        # Negative emotions resolved
        for neg in first_negative:
            transitions[(neg, "Improved Well-being")] += 1
    
    if not first_positive and last_positive:
        # New positive emotions developed
        for pos in last_positive:
            transitions[("Initial State", pos)] += 1
    
    # Track sustained positive emotions
    sustained_positive = first_positive & last_positive
    for pos in sustained_positive:
        transitions[(pos, "Sustained Positivity")] += 1

# Filter out transitions with very low counts to reduce clutter
filtered_transitions = {k: v for k, v in transitions.items() if v >= 3}

# Prepare data for Sankey diagram
source_nodes = []
target_nodes = []
values = []

for (source, target), value in filtered_transitions.items():
    source_nodes.append(source)
    target_nodes.append(target)
    values.append(value)

# Create ordered label list for clear left-to-right flow
all_labels_ordered = [
    # Starting states (left side)
    "Initial State",
    "Tired", "Sad", "Mad", "Anxious", "Worried", "Frustrated",
    # Positive emotions (middle)
    "Happy", "Relaxed", "Focused", "Excited",
    # Outcomes (right side)
    "Improved Well-being", "Sustained Positivity"
]

# Filter to only include labels that appear in our data
all_labels = [label for label in all_labels_ordered if label in set(source_nodes + target_nodes)]
label_to_index = {label: i for i, label in enumerate(all_labels)}

# Convert to indices
source_indices = [label_to_index[source] for source in source_nodes]
target_indices = [label_to_index[target] for target in target_nodes]

# Create colors for nodes
node_colors = []
for label in all_labels:
    if label in positive_emotions:
        node_colors.append('rgba(34, 139, 34, 0.9)')  # Forest green for positive emotions
    elif label in negative_emotions:
        node_colors.append('rgba(220, 20, 60, 0.9)')  # Crimson for negative emotions
    elif label in ["Improved Well-being", "Sustained Positivity"]:
        node_colors.append('rgba(0, 191, 255, 0.9)')  # Deep sky blue for outcomes
    else:
        node_colors.append('rgba(105, 105, 105, 0.8)')  # Dim gray for initial state

# Create dynamic link colors
link_colors = []
for source, target in zip(source_nodes, target_nodes):
    if source in negative_emotions and target in positive_emotions:
        link_colors.append('rgba(0, 255, 0, 0.7)')  # Bright green for improvement
    elif source in negative_emotions and target in ["Improved Well-being"]:
        link_colors.append('rgba(0, 206, 209, 0.7)')  # Dark turquoise for resolution
    elif source in positive_emotions and target in ["Sustained Positivity"]:
        link_colors.append('rgba(255, 215, 0, 0.7)')  # Gold for sustained positivity
    elif source == "Initial State":
        link_colors.append('rgba(70, 130, 180, 0.7)')  # Steel blue for new positive development
    else:
        link_colors.append('rgba(128, 128, 128, 0.5)')  # Gray for other transitions

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=1),
        label=all_labels,
        color=node_colors,
        x=[0.1 if label in ["Initial State"] + list(negative_emotions) 
           else 0.5 if label in positive_emotions
           else 0.85 for label in all_labels],
        y=[i*0.1 for i in range(len(all_labels))]
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title_text="Student Emotional Journey Through Platform Use<br><sub>From Initial State → Through Emotions → To Positive Outcomes</sub>",
    font_size=14,
    width=1400,
    height=800,
    margin=dict(l=50, r=50, t=100, b=50)
)

# Print summary statistics
print(f"Emotion transitions analyzed: {len(filtered_transitions)}")
print(f"Students with multiple check-ins: {len([g for _, g in check_in_df.groupby('studentId') if len(g) >= 2])}")
print("\nKey transitions (showing improvement):")
improvement_transitions = [(s, t, v) for (s, t), v in filtered_transitions.items() 
                          if s in negative_emotions and (t in positive_emotions or t == "Improved Well-being")]
for source, target, count in sorted(improvement_transitions, key=lambda x: x[2], reverse=True)[:10]:
    print(f"  {source} → {target}: {count} students")

fig.show()
