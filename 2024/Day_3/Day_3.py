class MulSearch:
    state = 0
    FSM = {}
    inputs = {}
    def __inti__(self):
        self.state = 0

        self.inputs = {0:{"digits":0,"value":0},
                      1:{"digits":0,"value":0}}

        self.FSM = {0:self.s0,
                    1:self.s1,
                    2:self.s2,
                    3:self.s3,
                    4:self.s4,
                    5:self.s5}
           
    def __call__(self, char:str):
        if self.state == 0:
            return self.s0(char)
        elif self.state == 1:
            return self.s1(char)
        elif self.state == 2:
            return self.s2(char)
        elif self.state == 3:
            return self.s3(char)
        elif self.state == 4:
            return self.s4(char)
        elif self.state == 5:
            return self.s5(char)
        else:
            raise Exeption
        
#        return self.FSM[self.state](char)

    def characterState(self,char,awaited_char):
        if char == awaited_char:
            self.state += 1
            return True
        else:
            self.reset()
            return False

    def digitState(self, char, input_idx, max_digits, end_char):
        if char.isdigit():
            if self.inputs[input_idx]["digits"] < max_digits:
                self.inputs[input_idx]["digits"] += 1

                self.inputs[input_idx]["value"] *= 10
                self.inputs[input_idx]["value"] += int(char)
            else:
                self.reset()
        else:
            if self.inputs[input_idx]["digits"] > 0:
                return self.characterState(char, end_char)
            else:
                self.reset()
        return False

    def reset(self):
        self.state = 0
        self.inputs = {0:{"digits":0,"value":0},
                       1:{"digits":0,"value":0}}

    def execute(self):
        if self.state != 6:
            raise Exception
        
        output = self.inputs[0]["value"] * self.inputs[1]["value"]
        self.reset()
        return output



# states
    def s0(self, char:str):
        self.characterState(char, "m")
        return False

    
    def s1(self, char:str):
        self.characterState(char, "u")
        return False
    
    def s2(self, char:str):
        self.characterState(char, "l")
        return False
    
    def s3(self, char:str):
        self.characterState(char, "(")
        return False

    def s4(self,char:str):
        self.digitState(char, 0, 3, ",")
        return False

    def s5(self, char:str):
        return self.digitState(char, 1, 3, ")")       

class EnableSearch:
    state = 0
    FSM = {}
    
    def __inti__(self):
        self.state = 0

        self.FSM = {0:self.s0,
                    1:self.s1,
                    2:self.s2,
                    3:self.s3}
           
    def __call__(self, char:str):
        if self.state == 0:
            return self.s0(char)
        elif self.state == 1:
            return self.s1(char)
        elif self.state == 2:
            return self.s2(char)
        elif self.state == 3:
            return self.s3(char)
        else:
            raise Exception
        
#        return self.FSM[self.state](char)

    def characterState(self,char,awaited_char):
        if char == awaited_char:
            self.state += 1
            return True
        else:
            self.reset()
            return False

    def reset(self):
        self.state = 0

# States
    def s0(self, char:str):
        self.characterState(char, "d")
        return False
    
    def s1(self, char:str):
        self.characterState(char, "o")
        return False
    
    def s2(self, char:str):
        self.characterState(char, "(")
        return False

    def s3(self,char:str):
        if self.characterState(char, ")"):
            self.reset()
            return True
        else:
            return False
        
class DisableSearch:
    state = 0
    FSM = {}
    
    def __inti__(self):
        self.state = 0

        self.FSM = {0:self.s0,
                    1:self.s1,
                    2:self.s2,
                    3:self.s3,
                    4:self.s4,
                    5:self.s5,
                    6:self.s6}
           
    def __call__(self, char:str):
        if self.state == 0:
            return self.s0(char)
        elif self.state == 1:
            return self.s1(char)
        elif self.state == 2:
            return self.s2(char)
        elif self.state == 3:
            return self.s3(char)
        elif self.state == 4:
            return self.s4(char)
        elif self.state == 5:
            return self.s5(char)
        elif self.state == 6:
            return self.s6(char)
        else:
            raise Exception
        
#        return self.FSM[self.state](char)

    def characterState(self,char,awaited_char):
        if char == awaited_char:
            self.state += 1
            return True
        else:
            self.reset()
            return False

    def reset(self):
        self.state = 0

# States
    def s0(self, char:str):
        self.characterState(char, "d")
        return False
    
    def s1(self, char:str):
        self.characterState(char, "o")
        return False
    
    def s2(self, char:str):
        self.characterState(char, "n")
        return False
    
    def s3(self, char:str):
        self.characterState(char, "'")
        return False
    
    def s4(self, char:str):
        self.characterState(char, "t")
        return False
    
    def s5(self, char:str):
        self.characterState(char, "(")
        return False

    def s6(self,char:str):
        if self.characterState(char, ")"):
            self.reset()
            return True
        else:
            return False
        
    

with open("Input", "r") as _file:
    _lines = _file.readlines()

    mul = MulSearch()
    mul_sum = 0
    mul_sum_conditional = 0

    enable = EnableSearch()
    disable = DisableSearch()
    enabled = True

    for line in _lines:
        for char in line:
            if enable(char):
                enabled = True
            if disable(char):
                enabled = False
            if mul(char):
                mul_result = mul.execute()
                mul_sum += mul_result
                mul_sum_conditional += (mul_result * enabled)
    print(mul_sum)
    print(mul_sum_conditional)
