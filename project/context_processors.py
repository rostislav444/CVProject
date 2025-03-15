import json
import os
from collections import OrderedDict

from django.conf import settings
from django.http import JsonResponse



def process_complex_object(obj):
    if isinstance(obj, (list, tuple)):
        return [process_complex_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: process_complex_object(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return process_complex_object(obj.__dict__)
    elif hasattr(obj, "__str__"):
        return str(obj)
    else:
        return repr(obj)


def get_settings_as_json_ordered():
    # Get the path to the settings.py file
    settings_file = settings.SETTINGS_MODULE.replace(".", "/") + ".py"
    settings_path = os.path.join(os.getcwd(), settings_file)

    # Read the file line by line to preserve order
    with open(settings_path, "r") as f:
        lines = f.readlines()

    # Extract user-defined settings in the order they are declared
    user_defined_settings = OrderedDict()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            parts = line.split("=", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                if hasattr(settings, key):
                    value = getattr(settings, key)
                    try:
                        json.dumps(value)
                        user_defined_settings[key] = value
                    except (TypeError, OverflowError):
                        user_defined_settings[key] = process_complex_object(value)

    return user_defined_settings


def settings_json(request):
    """Returns all Django settings in JSON format."""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    return JsonResponse(get_settings_as_json_ordered())


def settings_context(request):
    user_defined_settings = get_settings_as_json_ordered()
    return {"settings": user_defined_settings}
