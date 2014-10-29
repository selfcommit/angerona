import threading

def hack_thread_name_tween_factory(handler, registry):
    def hack_thread_name_tween(request):
        # Hack in the request ID inside the thread's name
        current_thread = threading.current_thread()
        original_name = current_thread.name
        current_thread.name = "%s][request=%s" % (original_name, request.id)
        try:
            response = handler(request)
        finally:
            # Restore the thread's original name when done
            current_thread.name = original_name
        return response
    return hack_thread_name_tween


