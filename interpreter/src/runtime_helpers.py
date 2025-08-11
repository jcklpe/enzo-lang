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
        return f"[{items}]"
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

def deep_copy_enzo_value(value):
    """Create a deep copy of an Enzo value (lists, tables, etc.)."""
    if isinstance(value, EnzoList):
        # Preserve the blueprint instance flag and name when copying
        new_list = EnzoList(
            is_blueprint_instance=getattr(value, '_is_blueprint_instance', False),
            blueprint_name=getattr(value, '_blueprint_name', None)
        )
        # Copy all elements
        for element in value._elements:
            new_list.append(deep_copy_enzo_value(element))
        # Copy key mapping
        new_list._key_map = value._key_map.copy()
        return new_list
    elif isinstance(value, (dict, Table)):
        # Deep copy dictionaries/tables
        new_dict = Table() if isinstance(value, Table) else {}
        for k, v in value.items():
            new_dict[k] = deep_copy_enzo_value(v)
        return new_dict
    elif isinstance(value, list):
        # Deep copy regular Python lists
        return [deep_copy_enzo_value(item) for item in value]
    else:
        # For primitive types (numbers, strings, functions), return as-is
        # Functions are immutable, primitives are copied by value
        return value

class EnzoList:
    """Enhanced list that supports both indexed and keyed access."""

    def __init__(self, is_blueprint_instance=False, blueprint_name=None):
        self._elements = []     # All elements in insertion order
        self._key_map = {}      # Maps key names to indices
        self._is_blueprint_instance = is_blueprint_instance  # Track if this came from a blueprint
        self._blueprint_name = blueprint_name  # Store blueprint name for proper printing

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
            # Exact match
            if k == key or k == f"${lookup_key}" or (k.startswith('$') and k[1:] == lookup_key):
                return self._elements[self._key_map[k]]

        # Try pattern matching: if looking for "name", try "name" + suffix patterns
        # This handles cases like looking for "name" and finding "$name6"
        if not lookup_key.isdigit():  # Don't do pattern matching for numeric keys
            for k in self._key_map:
                k_base = k[1:] if k.startswith('$') else k  # Remove $ prefix
                # Check if the stored key starts with the lookup key + digit suffix
                if k_base.startswith(lookup_key) and len(k_base) > len(lookup_key):
                    suffix = k_base[len(lookup_key):]
                    # If the suffix is numeric or a common separator + numeric, it's a match
                    if suffix.isdigit() or (suffix.startswith('-') and suffix[1:].isdigit()):
                        return self._elements[self._key_map[k]]

        raise KeyError(f"list property not found: ${lookup_key}")

    def set_by_key(self, key, value):
        """Set element by key name."""
        # Normalize key (remove $ prefix for lookup if present)
        lookup_key = key[1:] if key.startswith('$') else key

        # Try different key formats
        for k in self._key_map:
            # Exact match
            if k == key or k == f"${lookup_key}" or (k.startswith('$') and k[1:] == lookup_key):
                self._elements[self._key_map[k]] = value
                return

        # Try pattern matching: if looking for "x", try "x" + suffix patterns
        # This handles cases like looking for "x" and finding "$x12"
        if not lookup_key.isdigit():  # Don't do pattern matching for numeric keys
            for k in self._key_map:
                k_base = k[1:] if k.startswith('$') else k  # Remove $ prefix
                # Check if the stored key starts with the lookup key + digit suffix
                if k_base.startswith(lookup_key) and len(k_base) > len(lookup_key):
                    suffix = k_base[len(lookup_key):]
                    # If the suffix is numeric or a common separator + numeric, it's a match
                    if suffix.isdigit() or (suffix.startswith('-') and suffix[1:].isdigit()):
                        self._elements[self._key_map[k]] = value
                        return

        raise KeyError(f"list property not found: ${key}")

    def get_key_at_index(self, index):
        """Get the key name for the element at the given 0-based index."""
        if index < 0 or index >= len(self._elements):
            return None

        # Find the key that maps to this index
        for key, key_index in self._key_map.items():
            if key_index == index:
                return key

        # If no key found, this is a positional-only element
        return None

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

        list_content = f"[{', '.join(items)}]"

        # If this is a blueprint instance, prefix with blueprint name
        if self._is_blueprint_instance and self._blueprint_name:
            return f"{self._blueprint_name}{list_content}"
        else:
            return list_content

    def __eq__(self, other):
        """Check equality with another list or EnzoList."""
        if isinstance(other, EnzoList):
            # Compare elements and key mappings
            return (self._elements == other._elements and
                    self._key_map == other._key_map)
        elif isinstance(other, list):
            # Compare with regular Python list - only if no keys are set
            if self._key_map:
                return False  # EnzoList with keys can't equal plain list
            return self._elements == other
        return False

    def __hash__(self):
        """Make EnzoList hashable for use as dict keys."""
        # Convert key_map to a frozenset of items for hashing
        key_items = frozenset(self._key_map.items()) if self._key_map else frozenset()
        return hash((tuple(self._elements), key_items))
