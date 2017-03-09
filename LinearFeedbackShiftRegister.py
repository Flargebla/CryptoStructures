#
# LinearFeedbackShiftRegister.py
#       Author: Connor Zapfel
#       Date:   03/08/2017
#
#   This class models a LFSR. A LFSR is a shift register where the input bit
#   is a linear function of the previous bitset. Each bit is XOR'd together
#   to generate the next input bit.
#
#   To  use this object, you must first create it by providing it with a
#   binary number in string form representing the registers for example:
#
#           LFSR = LinearFeedbackShiftRegister("101101001")
#
#   You can cycle through iterations of the LFSR by using the step() function
#   to perform a shift as so:
#
#           LFSR.step()
#
#
class LinearFeedbackShiftRegister(object):
    #
    #   Initializes the LFSR with the provided bits
    #       iv - The string input of the bits to put in the register
    #
    def __init__(self, iv):
        self.iv = iv
        self.flipflops = []
        for bit in iv:
            self.flipflops.append(int(bit))
        self.output = ""

    #
    #   Returns the register bits as a string
    #
    def get_flipflops_as_bitstring(self):
        s = ""
        for i in self.flipflops:
            s += str(i)
        return s

    #
    #   Returns the number of bits in use
    #
    def get_size(self):
        return len(self.flipflops)

    #
    #   Returns the output bits currently generated
    #
    def get_output(self):
        return self.output
    
    #
    #   Clears the current output bits
    #
    def clear_output(self):
        self.output = ""

    #
    #   Shifts the register bits right once, and adds a 0 bit to input
    #
    def shift_right(self):
        self.flipflops = [0] + self.flipflops[0:-1]

    #
    #   Returns the calculated input bit
    #
    def calc_first_bit(self):
        temp = self.flipflops[-1] ^ self.flipflops[-2]
        vals = reversed(self.flipflops)
        for x in reversed(self.flipflops[0:-2]):
            temp = temp ^ x
        return temp

    #
    #   Runs a single iteration of the LFSR
    #
    def step(self):
        self.output += str(self.flipflops[-1])
        c = self.calc_first_bit()
        self.shift_right()
        self.flipflops[0] = c

    #
    #   Provides a print-friendly representation of the LFSR
    #
    def __str__(self):
        s = ""
        s += "-----     " * self.get_size()
        s += "\n"
        l = ["| {} | --> ".format(x) for x in self.flipflops]
        for i in l:
            s += i
        s += self.output
        s += "\n"
        s += "-----     " * self.get_size()
        return s
    
    #
    #   Resets the LFSR to its original state
    #
    def reset(self):
        self.__init__(self.iv)

    #
    #   Returns the period of the LFSR, or how many iterations are allowed
    #   until a cycle is found.
    #   NOTE: This calculation calls reset() and destroys any progress
    #
    def get_period(self):
        self.reset()
        p = 0
        list_of_seqs = []
        s = ""
        while s not in list_of_seqs:
            list_of_seqs.append(self.get_flipflops_as_bitstring())
            self.step()
            s = self.get_flipflops_as_bitstring()
            p += 1
        self.reset()
        return p
