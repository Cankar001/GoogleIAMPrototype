def acquire_input(prompt: str):
    success = True
    result = ''
    try:
        result = input(prompt)
    except KeyboardInterrupt:
        success = False

    return success, result

