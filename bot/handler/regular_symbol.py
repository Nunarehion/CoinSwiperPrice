import re

def escape_special(text):
    text = str(text)
    # Все специальные символы для MarkdownV2
    special_characters = r'[_*[\]()~`>#+\-=|{}.!]'
    
    # Экранируем специальные символы
    escaped_text = re.sub(special_characters, r'\\\g<0>', text)
    
    return escaped_text
