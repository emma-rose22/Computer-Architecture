"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.sp = self.reg[7]
        self.pc = 0
    
    def ram_read(self):
        ram_index = self.ram[self.pc + 1]
        self.pc += 2
        return self.ram[ram_index]

    def ram_write(self):
        where_save = self.ram[self.pc + 1]
        what_save = self.ram[self.pc + 2]
        self.ram[where_save] = what_save
        self.pc += 3


    def load(self):
        """Load a program into memory."""
        try:
            #our pointer
            address = 0

            #if I forgot to pass in a file name len(sys) == 1
            if len(sys.argv) < 2:
                print('Please pass in a second file name to use')
            file_name = sys.argv[1]

            #so I don't have to cd into example
            file_name = 'examples/' + file_name

            #auto closes file
            with open(file_name) as file:
                for line in file:
                    # split input away from notes
                    split_line = line.split('#')
                    #get whats before the notes and strip away new line characters
                    command = split_line[0].strip()
                    #skip over white space
                    if command == '':
                        continue 
                    
                    #convert from binary string to int
                    num = int(command, 2)
                    #actually inserting the instruction into the ram 
                    self.ram[address] = num
                    #increment the pointer
                    address += 1
        #not a real file
        except FileNotFoundError:
            print(f'{sys.argv[1]} file was not found.')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print('op', op)
        # print("ADD")

        if op == "ADD":
            #self.reg[reg_a] += self.reg[reg_b]
            added = self.reg[reg_a] + self.reg[reg_b]
            self.reg[reg_a] = added

        if op == "MUL":
            multiplied = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = multiplied
        else:
            # raise Exception("Unsupported ALU operation")
            pass

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #table of names for the commands
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        RET = 0b00010001
        ADD = 0b10100000
        PUSH = 0b01000101
        CALL = 0b01010000

        running = True
        while running == True:
    
            command = self.ram[self.pc]
            
            if command == HLT:
                #stop
                running = False
            if command == LDI:
                #save value in register
                #will have to move the counter to the register wanted
                #and then move it to the integer to be saved
                reg = self.ram[self.pc + 1] 
                integer = self.ram[self.pc + 2]
                self.reg[reg] = integer
                self.pc += 3

            if command == PRN:
                #print function
                #move the counter to go to the register
                #then print what is at that register
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])
                self.pc += 2

            if command == MUL:
                #multiplication function
                #the actual work will be implemented in the alu function
                #so here I just need to get the two addresses to be multiplied
                reg_1 = self.ram[self.pc + 1]
                reg_2 = self.ram[self.pc + 2]
                self.alu("MUL", reg_1, reg_2)
                self.pc += 3

            if command == ADD:
                reg_1 = self.ram[self.pc + 1]
                reg_2 = self.ram[self.pc + 2]
                self.alu("ADD", reg_1, reg_2)
                self.pc += 3

            if command == PUSH:
                #save value in ram
                #decrement stack pointer to get to where we want to push to
                self.sp -= 1
                #get register number from memory 
                #get value from register number
                value = self.reg[self.ram[self.pc + 1]]
                #at the stack pointer value in memory, insert the value
                self.ram[self.sp] = value
                #increment the program counter
                self.pc += 2

            if command == POP:
                #remove and return value from ram into register
                #get the register number from memory
                reg = self.ram[self.pc + 1]
                #uses stack pointer to get value from memory
                value = self.ram[self.sp]
                #put that value into the register at reg number
                self.reg[reg] = value
                #increment the stack pointer
                self.sp += 1
                #increment program counter
                self.pc += 2

            if command == CALL:
                #get register address is stored at 
                reg = self.ram[self.pc + 1]
                #get the address from the register
                address = self.reg[reg]
                #get the address to return to
                return_address= self.pc+2
                #decrement the stack pointer so we can save return address
                self.sp -= 1
                #save return address
                self.ram[self.sp] = return_address
                #now we can set the program counter to the address of 
                #the function we are trying to call
                self.pc = address

            if command == RET:
                #pop off the stack our return address
                return_address = self.ram[self.sp]
                #increment the stack pointer since we popped off
                self.sp += 1
                #set the program counter to the return address,
                #sending the program back on its way
                self.pc = return_address
