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
    plant_status = determine_plant_status(plant_health)

    st.title("Welcome to Fruit Productivity!")
    
    plant_species = st.text_input(
        "Before we get to work, what type of fruit would you like to grow with productivity?",
        key="plant_species"
    )

    st.write("Your plant is at " + str(plant_health) + " health points. It is now a " +
             plant_status + ". Let's get productive to grow your plant!")

    num_tasks_str = st.text_input("How many tasks do you have today?", key="num_tasks_input")
    
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

def countdown(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        st.title(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    st.header("Time's up!")

def do_tasks(to_do):
    minutes_worked, to_do, extra_tasks = points_and_task_completion(to_do)
    points_earned = sum(task[2] for task in to_do.values())
    tasks_completed = len(to_do)-len(extra_tasks)
    if minutes_worked != 0:
        st.write("You completed " + str(tasks_completed) + " tasks, worked for " + str(minutes_worked) + " minutes, and earned " + str(points_earned) + " points 🙌!!")
    return points_earned, tasks_completed, minutes_worked

def points_and_task_completion(task_list):
    minutes_worked = 0
    intervals_worked = 0
    tasks_left = {}
    points_earned = 0

    for i in range(len(task_list)):

        # lets users take a 15 min break after working for 1 hr
        if minutes_worked >= 60:
            intervals_worked += 1
            minutes_worked = 0
            st.title("You've been working hard! Let's take a short break!")
            countdown(15 * 60)

        # saves task info as variables
        task_name = task_list[i][0]
        task_num = i+1
        task_time = task_list[i][1]
        task_points = task_list[i][2]
    
        st.title("Let's start Task " + str(task_num) + ": " + task_name + ". You have " + str(task_time) + " minutes for this task.")
        st.write("Ready? GO!!")
        countdown(task_time * 60)

        # gives users time to finish task, gives them extra 1/4 of original time if they need it, adds points based on productivity
        finished = st.text_input("Are you finished with your task (yes/no)? ")
        if finished == "no":
            st.write("That's fine. Take a few more minutes. 🎗")
            #countdown(task_time * 15)
            finished = st.text_input("Finished (yes/no)? ")
            if finished == "no":
                to_do[i][2] = 0
                st.write("Brush it off. Let's move on to the next task. 👍")
                minutes_worked += task_time*1.25
                tasks_left[i] = task_list[i]
            elif finished == "yes":
                st.header("AWESOME!! You earned " + str(task_points) + " points for completing this task! 😎")
                points_earned += task_points
                minutes_worked += task_time*1.25
        elif finished == "yes":
            st.header("AWESOME!! You earned " + str(task_points) + " points for completing this task! 😎 ")
            points_earned += task_points
            minutes_worked += task_time
        minutes_worked = minutes_worked + intervals_worked*60
        return minutes_worked, task_list, tasks_left

def shop(user_points, plant_health, plant_species, tasks_completed):
    plant_status = determine_plant_status(plant_health)
    shop_items = {"items":["premium fertilizer", "normal fertilizer", "sun lamp", "growth potion", "water", "pruning tools", "a little love"], "costs":[200, 100, 200, 600, 80, 100, 10], "health_points": [20, 10, 20, 60, 8, 10, 1]}
    st.write(
        f"You have {user_points} points! Your plant health is now at {plant_health}, "
        f"and your {plant_species} is a {plant_status}!"
    )
    st.title("Productivity Shop")
    st.write("Buy items with your productivity points to help your fruit grow.")
    for i in range(len(shop_items["items"])):
        st.write("Item #" + str(i+1) + ": " + shop_items["items"][i] + ". Cost: " + str(shop_items["costs"][i]) + ". Benefits : +" + str(shop_items["health_points"][i]) + " plant health points.")
    st.header("How many items would you like to buy? ")
    num_items = int(st.text_input(""))
    for i in range(num_items):
        item_index = int(st.text_input("What item number would you like to buy for your plant? "))-1
        item_cost = shop_items["costs"][item_index]
        if item_cost <= user_points:
            user_points -= item_cost
            plant_health += shop_items["health_points"][item_index]
            plant_status = determine_plant_status(plant_health)
            st.header("Purchase complete! Your " + plant_species + " is now a " + plant_status + "!")
    st.title("Good work today! See you next time.")
    return plant_health, user_points

to_do, plant_health, plant_species = welcome()

if len(to_do) != {}:
    points_earned, tasks_completed, minutes_worked = do_tasks(to_do)

    if minutes_worked != 0:
        user_points += points_earned
    
        plant_health, user_points, minutes_worked = shop(user_points, plant_health, plant_species, tasks_completed)