# import glob
# import time

# old = set(glob.glob('*'))

# while True:
#     time.sleep(3)
#     new = set(glob.glob('*'))
    
#     if added := new-old:
#         print('Added :',' '.join(added))
#     if removed := old-new:
#         print('Removed :',' '.join(removed))
    
#     old = new

import psutil
print(f'CPU  :{psutil.cpu_percent(interval=1):5} %')
print(f'Memory  :{psutil.virtual_memory().percent:5} %')
print(f"Disk  :{psutil.disk_usage('/').percent:5} %")