from datetime import datetime
import logging

today = datetime.now()
log_file = f"{today.strftime('%Y%m%d')}.log"

def start_program(logger):
    def decorator(func):
        def start_log():
            # log_file = f"{datetime.now().strftime('%Y%m%d')}.log"
            # with open(log_file, 'w') as f:
            #     f.write(f"Program started at {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            #     return func()
            logger.info('Start program')
            return func()

        return start_log
    return decorator