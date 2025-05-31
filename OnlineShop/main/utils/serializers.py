from datetime import datetime, date
from decimal import Decimal

def custom_serializer(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (list, tuple, set)):
        return [custom_serializer(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: custom_serializer(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return custom_serializer(obj.__dict__)
    return obj