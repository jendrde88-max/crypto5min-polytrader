import time
now = int(time.time())
window = 300
current_start = (now // window) * window
next_start = current_start + window
remaining = next_start - now
print(f'Now: {now}')
print(f'Current window started: {current_start}')
print(f'Next window in: {remaining}s ({remaining//60}m {remaining%60}s)')
