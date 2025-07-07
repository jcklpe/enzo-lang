# Runtime helpers for Enzo language
# Provides Table class and format_val for pretty-printing Enzo runtime values

import os

# Always return the log path, but do NOT truncate the file here.
def _ensure_debug_log():
    # Updated path: interpreter/debugging/debug.log
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debugging", "debug.log")
    return log_path

class Table(dict):
    def __repr__(self):
        # Just use dict's items (no duplicates)
        items = []
        for key, val in self.items():
            items.append(f"{key}: {format_val(val)}")
        return "{ " + ", ".join(items) + " }"

def format_val(v):
    if isinstance(v, EnzoList):
        return repr(v)  # EnzoList has its own __repr__ method
    elif isinstance(v, Table) or (isinstance(v, dict) and not isinstance(v, list)):
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
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debugging", "debug.log")
    with open(log_path, "w"):
        pass

def log_debug(msg):
    pass  # Disable debug output
    # print(msg)  # Enable for debugging

class EnzoList:
    """Enhanced list that supports both indexed and keyed access."""

    def __init__(self):
        self._elements = []     # All elements in insertion order
        self._key_map = {}      # Maps key names to indices

    def append(self, value):
        """Add an element with automatic index."""
        self._elements.append(value)

    def set_key(self, key, value):
        """Set a key-value pair."""
        # Check if key already exists
        if key in self._key_map:
            # Update existing key
            index = self._key_map[key]
            self._elements[index] = value
        else:
            # Add new key-value pair
            self._key_map[key] = len(self._elements)
            self._elements.append(value)

    def get_by_index(self, index):
        """Get element by 1-based index."""
        if not isinstance(index, int) or index < 1 or index > len(self._elements):
            raise IndexError("list index out of range")
        return self._elements[index - 1]

    def get_by_key(self, key):
        """Get element by key name."""
        # Normalize key (remove $ prefix for lookup if present)
        lookup_key = key[1:] if key.startswith('$') else key

        # Try different key formats
        for k in self._key_map:
            if k == key or k == f"${lookup_key}" or (k.startswith('$') and k[1:] == lookup_key):
                return self._elements[self._key_map[k]]

        raise KeyError(f"list property not found: ${lookup_key}")

    def set_by_key(self, key, value):
        """Set element by key name."""
        # Find the actual key in the map
        for k in self._key_map:
            lookup_key = key[1:] if key.startswith('$') else key
            if k == key or k == f"${lookup_key}" or (k.startswith('$') and k[1:] == lookup_key):
                self._elements[self._key_map[k]] = value
                return
        raise KeyError(f"list property not found: ${key}")

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __setitem__(self, index, value):
        self._elements[index] = value

    def __iter__(self):
        return iter(self._elements)

    def __repr__(self):
        items = []
        for i, element in enumerate(self._elements):
            # Check if this element has a key
            key_for_index = None
            for k, idx in self._key_map.items():
                if idx == i:
                    key_for_index = k
                    break

            if key_for_index:
                items.append(f"{key_for_index}: {format_val(element)}")
            else:
                items.append(format_val(element))

        return f"[ {', '.join(items)} ]"
