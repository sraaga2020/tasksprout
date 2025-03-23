import time
import streamlit as st

user_points = 0


def determine_plant_status(plant_health):
    plant_stages = ["sprout", "flowering plant", "raw fruit", "ripe fruit"]
    plant_status = ""
    if 0 <= plant_health <= 20:
        plant_status = plant_stages[0]
    elif 20 <= plant_health <= 40:
        plant_status = plant_stages[1]
    elif 60 <= plant_health <= 80:
        plant_status = plant_stages[2]
    elif plant_health >= 80:
        plant_status = plant_stages[3]
    return plant_status

def welcome():  
    to_do = {}
    plant_health = 0
    plant_species = ""
    num_tasks_str = ""
    st.title("Welcome to Task Sprout! 🌱")
    
    plant_species = st.selectbox(
        'Choose a fruit to grow with your productivity!',
        ('','Watermelon 🍉', 'Strawberry 🍓', 'Tomato 🍅'))
    if plant_species != "":
        st.write("Awesome choice! Let's get productive to grow your plant!")
        num_tasks_str = st.text_input("How many tasks do you have today? ✍️", key="num_tasks_input")
    
    if num_tasks_str.isdigit():
        num_tasks = int(num_tasks_str)
        st.write("Enter your tasks in order of importance!")
        
        for i in range(num_tasks):
            task = st.text_input(f"Task {i+1}:", key=f"task_name_{i}")
            time_needed_str = st.text_input(f"Time required for Task {i+1} (in minutes):", key=f"task_time_{i}")
            
            if time_needed_str.isdigit():
                time_needed = int(time_needed_str)
                points = time_needed * 10
                to_do[i] = [task, time_needed, points]
    
    return to_do, plant_health, plant_species

def countdown(total_seconds):
    countdown_placeholder = st.empty()

    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        timer_str = f"{mins:02d}:{secs:02d}"
        countdown_placeholder.markdown(f"### ⏳ {timer_str}")
        time.sleep(1)
        total_seconds -= 1

    countdown_placeholder.markdown("Time's up! 🔔")

def do_tasks(to_do):
    result = points_and_task_completion(to_do)

    if result is None:
        return None, None, None

    minutes_worked, to_do, extra_tasks = result
    points_earned = sum(task[2] for task in to_do.values())
    tasks_completed = len(to_do) - len(extra_tasks)

    if minutes_worked != 0:
        st.write(f"You completed {tasks_completed} tasks, worked for {minutes_worked} minutes, and earned {points_earned} points 🙌!!")

    return points_earned, tasks_completed, minutes_worked


def points_and_task_completion(task_list):
    for key, default in {
        "task_index": 0,
        "waiting_extra": False,
        "points_earned": 0,
        "minutes_worked": 0,
        "tasks_left": {}
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    i = st.session_state.task_index

    if i >= len(task_list):
        st.success("🎉 All tasks processed!")
        return st.session_state.minutes_worked, task_list, st.session_state.tasks_left

    # Task info
    task_name, task_time, task_points = task_list[i]
    st.title(f"Task {i + 1}: {task_name}")
    st.write(f"You have {task_time} minutes.")
    finished = None

    if st.button("GO!", key=f"go_{i}"):
        countdown(task_time * 1)
        st.session_state[f"show_finished_{i}"] = True

    if st.session_state.get(f"show_finished_{i}", False):
        finished = st.text_input("Are you finished with your task? (yes/no)", key=f"finished_{i}").strip().lower()

    if finished == "no" and not st.session_state.waiting_extra:
        st.write("That's fine. Take some more time.")
        if st.button("Continue task", key=f"continue_{i}"):
            countdown(task_time * 1)
            st.session_state.waiting_extra = True

    if st.session_state.waiting_extra:
        finished_extra = st.text_input("Finished now? (yes/no)", key=f"finished_extra_{i}").strip().lower()
        if finished_extra == "yes":
            st.success(f"✅ You earned {task_points / 2} points!")
            st.session_state.points_earned += task_points / 2
            st.session_state.minutes_worked += task_time * 1.25
            st.session_state.waiting_extra = False
            st.session_state.task_index += 1
            st.rerun()
        elif finished_extra == "no":
            st.warning("Brush it off. No points earned.")
            task_list[i][2] = 0
            st.session_state.tasks_left[i] = task_list[i]
            st.session_state.minutes_worked += task_time * 1.25
            st.session_state.waiting_extra = False
            st.session_state.task_index += 1
            st.rerun()

    elif finished == "yes":
        st.success(f"✅ You earned {task_points} points!")
        st.session_state.points_earned += task_points
        st.session_state.minutes_worked += task_time
        st.session_state.task_index += 1
        st.rerun()



def shop(user_points, plant_health, plant_species, tasks_completed):
    plant_status = determine_plant_status(plant_health)
    shop_items = {"items":["premium fertilizer", "normal fertilizer", "sun lamp", "growth potion", "water", "pruning tools", "a little love"], "costs":[200, 100, 200, 600, 80, 100, 10], "health_points": [20, 10, 20, 60, 8, 10, 1]}
    st.title("Productivity Shop")
    st.write("Buy items with your productivity points to help your fruit grow. 📈")
    for i in range(len(shop_items["items"])):
        st.markdown(
            f"**Item #{i+1}**: {shop_items['items'][i]}.Cost: {shop_items['costs'][i]}. Benefits: +{shop_items['health_points'][i]} plant health points."
        )
    st.header("Checkout ")    
    item_index = st.text_input("What item number would you like to buy for your plant? ")
    if item_index:
        item_index = int(item_index)-1
        item_cost = shop_items["costs"][item_index]
        if item_cost <= user_points:
            user_points -= item_cost
            plant_health += shop_items["health_points"][item_index]
            plant_status = determine_plant_status(plant_health)
            st.header("Purchase complete 💰! Your " + plant_species + " has grown to a " + plant_status + " ! ❤️")
            st.title("Good work today! See you next time. 👋")
    return plant_health, user_points

to_do, plant_health, plant_species = welcome()
if len(to_do) != 0:
    points_earned, tasks_completed, minutes_worked = do_tasks(to_do)
    if minutes_worked != None:
        user_points += points_earned
        plant_health, user_points = shop(user_points, plant_health, plant_species, tasks_completed)
