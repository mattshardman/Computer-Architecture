"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111 
MUL = 0b10100010
HLT = 0b00000001 

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.branch_table = {
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            HLT: self.handle_hlt,
        }

    def load(self):
        """Load a program into memory."""
        f = open(sys.argv[1], "r")
        address = 0
        for line in f:
            ln = ''
            for char in line:
                if char == '#':
                    break
                if char == '\n':
                    break
                ln += char
            if len(ln) > 0:
                self.ram[address] = int(ln, 2)
            
        

    def ram_read(self, MAR):
        if MAR <= len(self.ram) - 1:
            return self.ram[MAR]
        return 0

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_ldi(self, op_a, op_b):
        self.reg[op_a] = op_b

    def handle_prn(self, op_a, _op_a):
        print(self.reg[op_a])

    def handle_mul(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)

    def handle_hlt(self, _op_a, _op_b):
        self.running = False

    def run(self):
        """Run the CPU."""
        while self.running:
        # set memory at pc counter to intruction register
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branch_table[ir](operand_a, operand_b)

            self.pc += 1 + (ir >> 6)

