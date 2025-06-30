# Runtime helpers for Enzo language
# Provides Table class and format_val for pretty-printing Enzo runtime values

import os

# Always return the log path, but do NOT truncate the file here.
def _ensure_debug_log():
    log_path = os.path.join(os.path.dirname(__file__), "logs", "debug.log")
    return log_path

class Table(dict):
    def __repr__(self):
        # Just use dict's items (no duplicates)
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

def clear_debug_log():
    log_path = os.path.join(os.path.dirname(__file__), "logs", "debug.log")
    with open(log_path, "w"):
        pass

def log_debug(msg):
    pass
    # print(msg)
