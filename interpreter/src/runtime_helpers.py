# Runtime helpers for Enzo language
# Provides Table class and format_val for pretty-printing Enzo runtime values

class Table(dict):
    def __repr__(self):
        items = []
        for key, val in self.items():
            items.append(f"{key}: {format_val(val)}")
        return "{ " + ", ".join(items) + " }"

def format_val(v):
    if isinstance(v, Table) or (isinstance(v, dict) and not isinstance(v, list)):
        # Use Enzo-style formatting for tables
        items = []
        for k, val in v.items():
            # Print $key: ... if key starts with $, else key: ...
            if isinstance(k, str) and k.startswith('$'):
                key_str = k
            elif isinstance(k, str):
                key_str = f"${k}" if k.isidentifier() else k
            else:
                key_str = str(k)
            items.append(f"{key_str}: {format_val(val)}")
        return f"{{ {', '.join(items)} }}"
    elif isinstance(v, list):
        items = ", ".join(format_val(el) for el in v)
        return f"[ {items} ]"
    elif isinstance(v, str):
        return f'"{v}"' if "\n" not in v else v
    elif callable(v):
        return str(v)
    else:
        return str(v)
