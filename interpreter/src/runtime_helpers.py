# Runtime helpers for Enzo language
# Provides Table class and format_val for pretty-printing Enzo runtime values

class Table(dict):
    def __repr__(self):
        items = []
        for key, val in self.items():
            items.append(f"{key}: {format_val(val)}")
        return "{ " + ", ".join(items) + " }"

def format_val(v):
    if isinstance(v, Table):
        items = ", ".join(f"{k}: {format_val(val)}" for k, val in v.items())
        return f"{{ {items} }}"
    elif isinstance(v, list):
        items = ", ".join(format_val(el) for el in v)
        return f"[ {items} ]"
    elif isinstance(v, str):
        return f'"{v}"' if "\n" not in v else v
    elif callable(v):
        return str(v)
    else:
        return str(v)
