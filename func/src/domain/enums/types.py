from enum import IntEnum


class QueueTypes(IntEnum):
    USER_UPDATE_REGISTER_DATA = 12

    def __repr__(self):
        return self.value
