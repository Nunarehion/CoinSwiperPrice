class mk:
    def __init__(self, st=''):
        self.st: str = st
        
    def indent(self, n=1):
        self.st += '\n'
        return self

    def bold(self):
        self.st = f'<b>{self.st}</b>'
        return self
    
    def italic(self):
        self.st = f'<i>{self.st}</i>'
        return self
        
    def under(self):
        self.st = f'<u>{self.st}</u>'
        return self
        
    def mono(self) -> str:
        self.st =  f"<code>{self.st}</code>"
        return self
        
    def code(self, language=''):
        self.st = f'<pre><code>{self.st}</code></pre>'
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
    
print("kukamongo")