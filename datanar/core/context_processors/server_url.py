def server_url(request):
    host = request.get_host()
    if "127.0.0.1" in host or "localhost" in host:
        return {"server_url": f"http://{host}"}
    return {"server_url": f"https://{host}"}


__all__ = ["server_url"]
