import random
from itertools import combinations

def generate_lab_groups(students, group_size, num_weeks, start_week=1, previous_groups=None, print_results=1, restarts=50):
    """
    Generates lab groups aiming to minimize repeat pairings between students.
    """
    history = {}
    
    def record_group(group):
        for pair in combinations(sorted(group), 2):
            history[pair] = history.get(pair, 0) + 1

    if previous_groups:
        for week in previous_groups:
            for group in week:
                record_group(group)
                
    all_weeks_groups = []
    
    def score_partition(partition):
        score = 0
        for group in partition:
            for pair in combinations(sorted(group), 2):
                score += history.get(pair, 0)
        return score

    for week in range(num_weeks):
        best_overall_partition = None
        best_overall_score = float('inf')
        
        for _ in range(restarts):
            shuffled = students[:]
            random.shuffle(shuffled)
            partition = [shuffled[i:i + group_size] for i in range(0, len(shuffled), group_size)]
            
            current_score = score_partition(partition)
            improved = True
            
            while improved:
                improved = False
                for i in range(len(partition)):
                    for j in range(i + 1, len(partition)):
                        for item1_idx in range(len(partition[i])):
                            for item2_idx in range(len(partition[j])):
                                
                                partition[i][item1_idx], partition[j][item2_idx] = \
                                partition[j][item2_idx], partition[i][item1_idx]
                                
                                test_score = score_partition(partition)
                                
                                if test_score < current_score:
                                    current_score = test_score
                                    improved = True
                                    break 
                                else:
                                    partition[i][item1_idx], partition[j][item2_idx] = \
                                    partition[j][item2_idx], partition[i][item1_idx]
                                    
                            if improved: break
                        if improved: break
                    if improved: break
            
            if current_score < best_overall_score:
                best_overall_score = current_score
                best_overall_partition = [list(g) for g in partition]
                
                if best_overall_score == 0:
                    break
                    
        for group in best_overall_partition:
            record_group(group)
            
        all_weeks_groups.append(best_overall_partition)

    schedule = all_weeks_groups

    if print_results == 1:
        num_weeks = len(schedule)
        # Find the maximum number of groups in any given week
        max_groups = max(len(week) for week in schedule)
    
        # 1. Print the Header Row
        headers = ["Group"] + [f"Week {start_week + i}" for i in range(num_weeks)]
        print("\t".join(headers))
    
        # 2. Print each Group's Block
        for group_idx in range(max_groups):
            # Find the max number of students for this group index across all weeks
            # (This ensures the block is tall enough even if some weeks have remainder groups)
            max_students = 0
            for week in schedule:
                if group_idx < len(week):
                    max_students = max(max_students, len(week[group_idx]))
            
            # Print a row for each student position in the group
            for student_idx in range(max_students):
                row = []
                
                # Column 1: Print the "Group X" label only on the first row of the block
                if student_idx == 0:
                    row.append(f"Group {group_idx + 1}")
                else:
                    row.append("")
                
                # Remaining Columns: Print the specific student for each week
                for week in schedule:
                    # Check if this group and student index actually exist for this week
                    if group_idx < len(week) and student_idx < len(week[group_idx]):
                        row.append(week[group_idx][student_idx])
                    else:
                        row.append("") # Leave blank if no student exists in this slot
                        
                print("\t".join(row))
            
            # Print an empty line to create a row gap between groups
            print()

        
    return all_weeks_groups


# ==========================================
# EXAMPLE USAGE
# ==========================================
if __name__ == "__main__":
    roster = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace", "Heidi", "Ivan"]
    
    # Example past groups
    past_groups = [
        [["Alice", "Bob", "Charlie"], ["Dave", "Eve", "Frank"], ["Grace", "Heidi", "Ivan"]]
    ]
    
    new_schedule = generate_lab_groups(
        students=roster, 
        group_size=3, 
        num_weeks=4, 
        previous_groups=past_groups
    )
