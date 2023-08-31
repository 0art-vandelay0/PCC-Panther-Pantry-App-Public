# **********************************************************************************************************************
# **********************************************************************************************************************
# Author:           Onyx Order of Programmers
# Date:             PCC Spring 2023 - CIS 234A
# Description:      This program manages notifications for the Panther Pantry
# Input:
# Output:
# Sources:
#
#
#
# Change Log:       - 04.22.2023: Program Base created from EAB code
#
# **********************************************************************************************************************
# **********************************************************************************************************************
from Logic.User import User
from UI.TabbedUI.TabbedUI import TabbedUI, launch_pantry


# TabbedUI Program Interface - Web Based

# function to launch the GUI that staff/managers will see upon login
def run_panther_pantry():
    launch_pantry()


# uncomment the below line for the program base to run
# run_panther_pantry()

# uncomment the below line to prove DB functionality
User.pull_user_data()
