"""
The chromosome is the set of values we wish to optimize with our algorithm. In this
it is the three gain values.
"""
class Chromosome:
    def __init__(self, kp, kd, ki):
        self.kp = kp
        self.kd = kd
        self.ki = ki

