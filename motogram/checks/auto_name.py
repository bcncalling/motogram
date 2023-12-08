from enum import Enum

class Auto_name(Enum):
    def _generate_next_value_(self, *args):
        return self.name.lower()

    def __repr__(self):
        return f"motogram.checks.{self.name}"
