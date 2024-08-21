def server_url(request):
    if "127.0.0.1" in request.get_host():
        return {"server_url": f"http://{request.get_host()}"}
    if "localhost" in request.get_host():
        return {"server_url": f"http://{request.get_host()}"}
    return {"server_url": f"https://{request.get_host()}"}


__all__ = ["server_url"]
