# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 10:36:13 2014

@author: zhihuixie
"""
import math
def resources_vs_time(upgrade_cost_increment, num_upgrade):
    """
    Build function that performs unit upgrades with specified cost increments
    """
    count_upgrade = 0
    time_resource = []
    resource = 0
    time =0
    while count_upgrade < num_upgrade:
        upgrade_cost = 1 + upgrade_cost_increment*count_upgrade
        resource += upgrade_cost
        time += upgrade_cost / (count_upgrade + 1)
        time_resource.append([math.log(time), math.log(resource)])
        count_upgrade += 1
    return time_resource
data1 = resources_vs_time(0.0, 10)
data2 = resources_vs_time(1.0, 10)
print data1, len(data1)
print data2, len(data2)