class brainfuck:
  def __init__(self):
    self.head = 0
    self.tape = bytearray(30000)
  
  def run(self, program):
    counter = 0
    
    while counter < len(program):
      if program[counter] == '>':
        self.head += 1
      elif program[counter] == '<':
        self.head -= 1
      elif program[counter] == '+':
        self.tape[self.head] = (self.tape[self.head] + 1) % 256
      elif program[counter] == '-':
        self.tape[self.head] = (self.tape[self.head] - 1) % 256
      elif program[counter] == '.':
        print(chr(self.tape[self.head]), end='')
      elif program[counter] == ',':
        self.tape[self.head] = ord(input()[0])
      elif program[counter] == '[':
        if self.tape[self.head] == 0:
          counter += 1
          level = 1
          while level != 0:
            if program[counter] == '[':
              level += 1
            if program[counter] == ']':
              level -= 1
            counter += 1
      elif program[counter] == ']':
        if self.tape[self.head] != 0:
          counter -= 1
          level = 1
          while level != 0:
            if program[counter] == '[':
              level -= 1
            if program[counter] == ']':
              level += 1
            counter -= 1
      counter += 1

if __name__ == "__main__":
  bf = brainfuck();
  bf.run("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
  