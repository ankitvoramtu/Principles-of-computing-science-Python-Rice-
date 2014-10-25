# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 21:09:57 2014

@author: zhihuixie
"""

"""
Cookie Clicker Simulator
You should first implement the ClickerState class. This class will encapsulate many of the variables that you used in implementing resources_vs_time in the homework and keep track of the state of the game during a simulation. By encapsulating the game state in this class, the logic for running a simulation of the game will be greatly simplified. The ClickerState class must keep track of four things:

The total number of cookies produced throughout the entire game (this should be initialized to 0.0).
The current number of cookies you have (this should be initialized to 0.0).
The current time (in seconds) of the game (this should be initialized to 0.0).
The current CPS (this should be initialized to 1.0).
Note that you should use floats to keep track of all state. You will have fractional values for cookies and CPS throughout.

During a simulation, upgrades are only allowed at an integral number of seconds as required in Cookie Clicker. (Upgrades will not be allowed at fractional seconds as in the homework). However, the CPS value is a floating point number. In addition to this information, your ClickerState class must also keep track of the history of the game. We will track the history as a list of tuples. Each tuple in the list will contain 4 values: a time, an item that was bought at that time (or None), the cost of the item, and the total number of cookies produced by that time. This history list should therefore be initialized as [(0.0, None, 0.0, 0.0)].

The methods of the ClickerState class interact with this state as follows:

__str__: This method should return the state (without the history list) as a string in a human readable format. This is primarily to help you develop and debug your program.
get_cookies, get_cps, get_time, get_history: These methods should simply return the current number of cookies, the current CPS, the current time, and the history, respectively.
time_until: This method should return the number of seconds you must wait until you will have the given number of cookies. Remember that you cannot wait for fractional seconds, so while you should return a float it should not have a fractional part.
wait: This method should "wait" for the given amount of time. This means you should appropriately increase the time, the current number of cookies, and the total number of cookies.
buy_item: This method should "buy" the given item. This means you should appropriately adjust the current number of cookies, the CPS, and add an entry into the history.
If you are passed an argument that is invalid (such as an attempt to buy an item for which you do not have enough cookies), you should just return from the method without doing anything.
"""

"""
Cookie Clicker Simulator
"""
import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._totalcookies = 0.0
        self._currcookies = 0.0
        self._currtime = 0.0
        self._currcps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._currtime) + " Current Cookies: " + str(self._currcookies) +" CPS: " + str(self._currcps) +" Total Cookies: " + str(self._totalcookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._currcookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._currcps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._currtime
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies - self._currcookies <=0 :
            return 0.0
        else:
            return math.ceil((cookies - self._currcookies)/self._currcps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0.0:
            self._currtime += time
            self._currcookies += time*self._currcps
            self._totalcookies += time*self._currcps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._currcookies:
            self._history.append((self._currtime, item_name, cost, self._totalcookies))
            self._currcps += additional_cps
            self._currcookies = self._currcookies - cost
            #self.history_list.append((self.current_time, item_name, cost, self.current_time*self.current_cps))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    new_build_info = build_info.clone()
    new_clicker_state = ClickerState()
    timer = new_clicker_state.get_time()
    #time_left = duration - timer
    while timer <= duration:
        item = strategy(new_clicker_state.get_cookies(), new_clicker_state.get_cps(), duration - timer, new_build_info)
        if item != None:
           item_cost = new_build_info.get_cost(item)
        if item == None:
            break
        #upgrade_time = NewClickerState.time_until(new_build_info.get_cost(item))
        elif duration < new_clicker_state.time_until(item_cost) + timer:
             break
       
        else:
            new_clicker_state.wait(new_clicker_state.time_until(item_cost))
            new_clicker_state.buy_item(item, item_cost, new_build_info.get_cps(item))
  
        new_build_info.update_item(item)
        timer = new_clicker_state.get_time()

    new_clicker_state.wait(duration - timer)
    return new_clicker_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    This is a cheapest strategy that you can use to help debug
    your simulate_clicker function.
    """
    new_build = build_info.clone()
    items = new_build.build_items()
    lowest = float("inf")
    for item in items:
        if new_build.get_cost(item) < lowest:
            lowest = new_build.get_cost(item)
            cheap = item
    if lowest > cps * time_left:
        return None
    else:
        return cheap

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    This is a expensive strategy that you can use to help debug
    your simulate_clicker function.
    """
    new_build = build_info.clone()
    items = new_build.build_items()
    highest = float("-inf")
    for item in items:
        if cookies + cps*time_left >= new_build.get_cost(item):  
            if new_build.get_cost(item) > highest:
                highest = new_build.get_cost(item)
                expensive = item
    if highest > cookies + cps*time_left or highest == float("-inf"):
        return None
    else:
        return expensive
     


def strategy_best(cookies, cps, time_left, build_info):
    """
    This is a best strategy that you can use to help debug
    your simulate_clicker function.
    """
    new_build = build_info.clone()
    items = new_build.build_items()
    return random.choice(items)
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", 1000, strategy_cursor)
    run_strategy(None, 1000, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", 1000, strategy_cheap)
    run_strategy("Expensive", 1000, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()

  
import user34_GhjnBEJSmI_10 as test_suite
test_suite.run_simulate_clicker_tests(simulate_clicker,strategy_none,strategy_cursor)
test_suite.run_clicker_state_tests(ClickerState)


