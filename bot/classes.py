class mk:
    def __init__(self, st='', escape='true'):
        if escape:
          st = st
        self.st = st
        
    def escape_markdown(self, text):
        print(text)
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'{char}')
        print(text)
        return text
        
    def indent(self, n = 1):
        self.st += '\n'
        return self

    def bold(self):
        self.st = f'***{self.st}***'
        return self
    
    def italic(self):
        self.st = f'_{self.st}_'
        return self
        
    def under(self):
        self.st = f'__{self.st}__'
        
    def mono(self):
        self.st = f'`{self.st}`'
        return self
        
    def code(self, language=''):
        self.st = f'```{language}\n{self.st}```'
        return self
        
    def align(self, width=9):
        parts = self.st.split(':')
        if len(parts) == 2:
            first_part_length = len(parts[0])
            spaces_to_add = max(0, width - first_part_length)
            self.st = f"{parts[0]}: {' ' * spaces_to_add}{parts[1].strip()}"
        return self

    def __repr__(self):
        return self.st
        
    def __add__(self, other):
        if isinstance(other, mk):
            return mk(self.st + '\n' + other.st)
        return mk(self.st + '\n' + str(other))

    def __radd__(self, other):
        return mk(str(other) + self.st)
        
    def __sub__(self, other):
        if isinstance(other, mk):
            return mk(self.st + other.st)
        return mk(self.st + str(other))