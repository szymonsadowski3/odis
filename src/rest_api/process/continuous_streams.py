MINUTE = 60


def get_stream_dictionary(stream_start, stream_end, total_time, records_in_stream):
    return {
        "stream_start": stream_start,
        "stream_end": stream_end,
        "total_time_in_seconds": total_time,
        "records_in_stream": records_in_stream,
    }

def get_final_stream(current_stream):
    stream_start = current_stream[0]["timestamp_start"]
    stream_end = current_stream[-1]["timestamp_start"]
    total_time_in_seconds = (stream_end - stream_start).seconds
    stream_dictionary = get_stream_dictionary(stream_start, stream_end, total_time_in_seconds, current_stream)
    return stream_dictionary

def find_continuous_streams(records):
    streams = []

    previous_record = None
    current_stream = []
    start_over = False
    records_length = len(records)

    for index, record in enumerate(records):
        if (index == 0) or start_over:
            current_stream.append(record)
            previous_record = record
            start_over = False
            continue
        timedelta = record["timestamp_start"] - previous_record["timestamp_start"]
        if timedelta.seconds < 5*MINUTE:
            current_stream.append(record)
            previous_record = record
            if index == records_length - 1:
                stream_dictionary = get_final_stream(current_stream)
                streams.append(stream_dictionary)
        else:
            stream_dictionary = get_final_stream(current_stream)
            streams.append(stream_dictionary)
            current_stream = []
            start_over = True

    return streams
