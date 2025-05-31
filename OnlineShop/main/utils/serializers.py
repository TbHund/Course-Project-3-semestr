class SimpleSerializer:
    @staticmethod
    def serialize(obj, indent=None, current_indent=0):
        if indent is None:
            return SimpleSerializer._serialize_compact(obj)
        return SimpleSerializer._serialize_spaces(obj, indent, current_indent)

    @staticmethod
    def _serialize_compact(obj):
        if obj is None:
            return 'null'
        elif isinstance(obj, bool):
            return 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(obj, list):
            items = [SimpleSerializer.serialize(item) for item in obj]
            return f'[{",".join(items)}]'
        elif isinstance(obj, dict):
            items = []
            for key, value in obj.items():
                if not isinstance(key, str):
                    raise TypeError("Ключи словаря должны быть строками")
                serialized_key = SimpleSerializer.serialize(key)
                serialized_value = SimpleSerializer.serialize(value)
                items.append(f'{serialized_key}:{serialized_value}')
            return f'{{{",".join(items)}}}'
        else:
            raise TypeError(f"Неподдерживаемый тип: {type(obj)}")

    #для вывода с отступами
    @staticmethod
    def _serialize_spaces(obj, indent, current_indent):
        if obj is None:
            return 'null'
        elif isinstance(obj, bool):
            return 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(obj, list):
            if not obj:
                return '[]'
            
            items = []
            for item in obj:
                serialized = SimpleSerializer._serialize_spaces(item, indent, current_indent + indent)
                items.append(' ' * (current_indent + indent) + serialized)
            
            return '[\n' + ',\n'.join(items) + '\n' + ' ' * current_indent + ']'
        
        elif isinstance(obj, dict):
            if not obj:
                return '{}'
            
            items = []
            for key, value in obj.items():
                if not isinstance(key, str):
                    raise TypeError("Ключи словаря должны быть строками")
                
                serialized_key = SimpleSerializer._serialize_spaces(key, indent, current_indent + indent)
                serialized_value = SimpleSerializer._serialize_spaces(value, indent, current_indent + indent)
                items.append(' ' * (current_indent + indent) + f'{serialized_key}: {serialized_value}')
            
            return '{\n' + ',\n'.join(items) + '\n' + ' ' * current_indent + '}'
        
        else:
            raise TypeError(f"Неподдерживаемый тип: {type(obj)}")


    @staticmethod
    def deserialize(s):
        s = s.strip()
        
        if s == 'null':
            return None
        elif s == 'true':
            return True
        elif s == 'false':
            return False
        
        #числа
        if s.lstrip('-').replace('.', '', 1).isdigit():
            return float(s) if '.' in s else int(s)
        
        #строки
        if s.startswith('"') and s.endswith('"'):
            return SimpleSerializer._parse_string(s[1:-1])
        
        #списки
        if s.startswith('[') and s.endswith(']'):
            return SimpleSerializer._parse_list(s[1:-1])
        
        #словари
        if s.startswith('{') and s.endswith('}'):
            return SimpleSerializer._parse_dict(s[1:-1])
        
        raise ValueError(f"Нераспознанный формат: {s}")

    #методы для десериализации
    @staticmethod
    def _parse_string(s):
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                if i + 1 < len(s):
                    next_char = s[i+1]
                    if next_char in ['\\', '"']:
                        result.append(next_char)
                        i += 2
                    else:
                        result.append('\\' + next_char)
                        i += 2
                else:
                    result.append('\\')
                    i += 1
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)

    @staticmethod
    def _parse_list(s):
        items = []
        start = 0
        depth = 0
        in_string = False
        
        for i, char in enumerate(s):
            if char == '"' and (i == 0 or s[i-1] != '\\'):
                in_string = not in_string
            elif not in_string:
                if char == '[' or char == '{':
                    depth += 1
                elif char == ']' or char == '}':
                    depth -= 1
                elif char == ',' and depth == 0:
                    items.append(s[start:i])
                    start = i + 1
        
        items.append(s[start:])
        return [SimpleSerializer.deserialize(item) for item in items if item.strip()]

    @staticmethod
    def _parse_dict(s):
        items = []
        start = 0
        depth = 0
        in_string = False
        
        for i, char in enumerate(s):
            if char == '"' and (i == 0 or s[i-1] != '\\'):
                in_string = not in_string
            elif not in_string:
                if char == '[' or char == '{':
                    depth += 1
                elif char == ']' or char == '}':
                    depth -= 1
                elif char == ',' and depth == 0:
                    items.append(s[start:i])
                    start = i + 1
        
        items.append(s[start:])
        
        result = {}
        for item in items:
            if not item.strip():
                continue
            key_part, value_part = item.split(':', 1)
            key = SimpleSerializer.deserialize(key_part.strip())
            value = SimpleSerializer.deserialize(value_part.strip())
            result[key] = value
        return result