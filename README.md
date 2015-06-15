# Analysis-of-CAN-bus-data-in-automobiles

Here, we analyse signal data received from CAN bus in a car to determine the driving pattern of a car driver, and then evaluate eligibility for safe-driver price reduction for vehicle insurance.

We parse the signal data from several sensors in the JSON file, and determine the times at which there were abrupt speed changes or gear shifts. We also view the locations where the speed was zero on google maps and determine if the driver stopped at locations he was supposed to.
