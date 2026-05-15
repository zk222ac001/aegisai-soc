def extract_features(
    src_port,
    dst_port,
    protocol,
    packet_count,
    byte_count,
    duration
):

    protocol_map = {
        "TCP": 1,
        "UDP": 2,
        "OTHER": 0
    }

    features = [
        src_port or 0,
        dst_port or 0,
        protocol_map.get(protocol, 0),
        packet_count or 0,
        byte_count or 0,
        duration or 0
    ]
    
    return features