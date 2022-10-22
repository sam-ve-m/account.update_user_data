from enum import IntEnum


class QueueTypes(IntEnum):
    USER_UPDATE_REGISTER_DATA = 12
    USER_UPDATE_RISK_DATA = 26

    def __repr__(self):
        return str(self.value)
