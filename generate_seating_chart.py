import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_seating_chart(names, excluded_names=None, seed=None):
    """
    Randomizes a list of names (excluding specified ones) and plots them 
    proportionally around a U-shaped table.
    """
    # 1. Handle exclusions
    if excluded_names is None:
        excluded_names = []
        
    # Filter names and get the final count
    attendees = [name for name in names if name not in excluded_names]
    N = len(attendees)
    
    if N > 16:
        raise ValueError(f"This table only seats up to 16 people. You provided {N} after exclusions.")
    if N == 0:
        print("No attendees to seat after exclusions!")
        return
        
    # 2. Randomize the filtered names
    rng = random.Random(seed) 
    shuffled = attendees[:]
    rng.shuffle(shuffled)
    
    # 3. Distribute seats proportionally based on table capacity (4 : 8 : 4)
    # This ensures an even spread across the entire U-shape.
    n_left = round(N * 0.25)
    n_right = round(N * 0.25)
    
    # Cap sides at 4
    if n_left > 4: n_left = 4
    if n_right > 4: n_right = 4
        
    n_bottom = N - n_left - n_right
    
    # If bottom somehow exceeds its 8 capacity, push overflow to the sides
    if n_bottom > 8:
        overflow = n_bottom - 8
        n_bottom = 8
        while overflow > 0:
            if n_left < 4:
                n_left += 1
                overflow -= 1
            if overflow > 0 and n_right < 4:
                n_right += 1
                overflow -= 1

    # 4. Dynamically calculate centered coordinates for each side
    # Format: (x, y, horizontal_alignment, vertical_alignment, rotation)
    seats = []
    
    # Left side (centered vertically around Y=3.5, spaced by 1.0)
    for i in range(n_left):
        y = 3.5 + (n_left - 1) / 2.0 - i
        seats.append((0.8, y, 'right', 'center', 0))
        
    # Bottom side (centered horizontally around X=5.5, spaced by 1.0)
    for i in range(n_bottom):
        x = 5.5 - (n_bottom - 1) / 2.0 + i
        seats.append((x, 0.2, 'right', 'top', 45))
        
    # Right side (centered vertically around Y=3.5, spaced by 1.0)
    for i in range(n_right):
        y = 3.5 - (n_right - 1) / 2.0 + i
        seats.append((10.2, y, 'left', 'center', 0))

    # 5. Setup the figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Draw the U-Shaped table
    table_coords = [
        (1, 5.5), (1, 0.5), (10, 0.5), (10, 5.5),  # Outer edge
        (9, 5.5), (9, 1.5), (2, 1.5), (2, 5.5)     # Inner edge
    ]
    u_table = patches.Polygon(
        table_coords, 
        closed=True, 
        facecolor='#D2B48C',   
        edgecolor='#8B4513',   
        linewidth=3
    )
    ax.add_patch(u_table)
    
    # 6. Place the text boxes for the names
    box_style = dict(boxstyle="round,pad=0.4", facecolor="#E6F2FF", edgecolor="#0066CC", linewidth=1.5)
    
    for i, name in enumerate(shuffled):
        x, y, ha, va, rot = seats[i]
        # CHANGED: Increased font size back up to 10
        ax.text(x, y, name, ha=ha, va=va, rotation=rot, fontsize=10, fontweight='bold', bbox=box_style)

    # 7. Finalize plot aesthetics
    ax.set_xlim(-3, 14)   
    ax.set_ylim(-2.5, 7)  
    ax.axis('off')        
    # CHANGED: Title removed
    
    plt.tight_layout()
    plt.show()
