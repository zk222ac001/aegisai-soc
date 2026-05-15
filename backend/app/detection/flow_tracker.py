flows = {}
def track_flow(src_ip, dst_ip, src_port, dst_port):
    key = f"{src_ip}:{src_port}-{dst_ip}:{dst_port}"

    if key not in flows:
        flows[key] = 0

    flows[key] += 1

    return flows[key]